from requests import Request, Session
from StringIO import StringIO

import json
import csv
import subprocess
import time

try:
  import pandas
except:
  pandas = False

VALID_GET_PARAMS = ['limit', 'start', 'gt', 'lt', 'gte', 'lte', \
    'reverse', 'version', 'style', 'since', 'tail', 'live', 'type']

class DatServerError(Exception):
  def __init__(self, resp):
    self.resp = resp
    self.resp_content = json.loads(resp.content)

    if self.resp_content.get('conflict'):
      message = self.resp_content['error']
    else:
      message = "Unknown server error. Received status code %s" % (self.resp_content['status'])
    super(DatServerError, self).__init__(message)

class LocalDat:

  def __init__(self, location=None):
    if location:
      subprocess.call(["cd", self.location])
      self.location = location

  def call(self, args, shell=True):
    return subprocess.call(args, shell=shell)

  def init(self):
    return self.call(["dat init --no-prompt"])

  def listen(self):
    p = subprocess.Popen("dat listen", shell=True)
    while p.poll == None:
      time.sleep(.5)
      p.poll()

    self.server = p
    return self.server

  def close(self):
    return subprocess.Popen.terminate(self.server)

  def clean(self):
    return self.call(["dat clean"])


class Dat:

  def __init__(self, host, username=None, password=None):
    # strip trailing slash
    self.host = host.strip('/')
    self.api_base = '{}/api'.format(self.host)
    self.auth = (username, password)
    print self.info()

  def api(self, resource, method, data=None, opts=None, stream=False):
    """
    Calls the dat with the given api specification

    Parameters:
    -----------

    resource: string
      the api resource to access. (e.g. 'rows', 'csv', 'session')
    method: string
      the http method to use. (e.g., 'GET', 'PUT')
    data: object (optional)
      optional arguments to be sent into raw body data (e.g., on post)
    opts: object (optional)
      optional arguments to be entered into query parameters
    stream: boolean (optional, default False)
      whether to stream the response
    """
    url = '%s/%s' % (self.api_base, resource)

    if data is None:
      data = {}
    if opts is None:
      opts = {}

    params = {}
    for param in VALID_GET_PARAMS:
      if opts.get(param):
        params[param] = opts[param]

    headers = {}
    data_format = opts.get('type')
    if data_format == 'csv':
      headers['content-type'] = 'text/csv'
    elif data_format == 'json':
      headers['content-type'] = 'application/json'

    req = Request(method, url, params=params, data=data, headers=headers)

    s = Session()
    if self.auth:
        s.auth = self.auth

    prepped = s.prepare_request(req)
    resp = s.send(prepped, stream=stream)
    if resp.status_code == 200 or resp.status_code == 201:
      return resp
    raise DatServerError(resp)

  def json(self, *args, **kwargs):
    resp = self.api(*args, **kwargs)
    return json.loads(resp.content)

  def info(self):
    return self.json('', 'GET')

  def changes(self, opts=None):
    resp = self.json('changes', 'GET', opts=opts)
    return resp['rows']

  def session(self):
    return self.json('session', 'GET')

  def to_csv(self):
    return self.api('csv', 'GET').content

  def rows(self, opts=None):
    resp = self.json('rows', 'GET', opts=opts)
    return resp['rows']

  def put(self, data, format='json', opts=None):
    """
    Put some rows in the dat.

    Parameters
    -----------
    data: generator, file, or dictionary

    """
    if opts is None:
      opts = {}

    opts['type'] = format

    # decode data into string
    if type(data) == dict:
      data = json.dumps(data)

    if type(data) == list:
      io = StringIO()
      for row in data:
        io.write(json.dumps(data))
        io.write('\n')
      data = io

    elif pandas and type(data) == pandas.core.frame.DataFrame:
      return self.put_pandas_dataframe(data, opts)

    return self.json('rows', 'POST', data=data, opts=opts)

  def put_pandas_dataframe(self, df, opts=None):
    if opts is None:
      opts = {}

    opts['type'] = 'json'

    def ndjson_gen(df_gen):
      ndjson = []
      row = True
      while row:
        try:
          row = next(generator)
          yield row[1].to_dict()
        except StopIteration:
          row = None

    return self.json('rows', 'POST', data=ndjson_gen(df.iterrows()), opts=opts)

  def to_pandas(self):
    if not pandas:
      print "Could not find pandas in this environment. Do you have it installed?"
      return False

    return pandas.read_csv(self.api_base + '/csv')





