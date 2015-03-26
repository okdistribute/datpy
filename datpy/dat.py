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
    message = "Unknown server error. Received status code %s" % (self.resp.status_code)

    try:
      self.resp_content = json.loads(resp.content)
      if self.resp_content.get('conflict'):
        message = self.resp_content['error']
    except:
      pass

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
    p = subprocess.Popen("dat listen", stdout=subprocess.PIPE, shell=True)
    while p.stdout.read(1) == None:
      time.sleep(.5)

    self.server = p
    return self.server

  def close(self):
    return subprocess.Popen.terminate(self.server)

  def clean(self):
    return self.call(["dat clean"])


class DatAPI:

  def __init__(self, host, username=None, password=None):
    # strip trailing slash
    self.host = host.strip('/')
    self.api_base = '{}/api'.format(self.host)
    self.creds = (username, password)
    self.info()

  def auth(self, username, password):
    """
    Sets up the internal auth object. Uses basic authentication.
    """
    self.creds = (username, password)

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
      optional arguments to be sent as query parameters to the endpoint
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
    if self.creds:
        s.auth = self.creds

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

  def put(self, data, format='json', opts=None):
    """
    Put some rows in the dat.

    Parameters
    -----------
    data: dictionary or pandas data frame
    format: string
    opts: object
      options to pass as GET parameters to the endpoint

    """
    if opts is None:
      opts = {}

    opts['type'] = format

    # decode data into string
    if type(data) == dict:
      data = json.dumps(data)
      return self.json('rows', 'POST', data=data, opts=opts)
    elif pandas and type(data) == pandas.core.frame.DataFrame:
      return self.put_pandas(data, opts)

  def put_bulk(self, file_or_buffer, format='json', opts=None):
    if opts is None:
      opts = {}

    opts['type'] = format

    return self.api('bulk', 'POST', data=file_or_buffer, opts=opts, stream=True)

  def put_pandas(self, df, opts=None):
    """
    Parameters
    ----------
    df: pandas dataframe
    opts: object
      options to pass as GET parameters to the endpoint
    """
    if opts is None:
      opts = {}

    opts['type'] = 'json'

    def generate_ndjson(generator):
      row = True
      while row:
        try:
          row = next(generator)
          yield row[1].to_json()
          yield '\n'
        except StopIteration:
          row = None

    generator = df.iterrows()

    return self.api('bulk', 'POST', data=generate_ndjson(generator), opts=opts, stream=True)

  def rows(self, opts=None):
    resp = self.json('rows', 'GET', opts=opts)
    return resp['rows']

  def to_file(self, file_or_buffer, format='csv', opts=None):
    """
    Output the data in a dat to a file.

    Parameters
    ----------
    file_or_buffer: object
      a file pointer created with `open` or a buffer (i.e., stringIO)
    """
    if not opts:
      opts = {}

    if format == 'csv':
      endpoint = 'csv'
    elif format == 'json':
      endpoint = 'rows'

    opts['live'] = True

    CHUNK_SIZE = 86

    resp = self.api(endpoint, 'GET', opts=opts, stream=True)
    for chunk in resp.iter_content(chunk_size=CHUNK_SIZE):
      file_or_buffer.write(chunk)

    return resp

  def to_json(self, opts=None):
    return self.rows(opts=opts)

  def to_csv(self):
    return self.api('csv', 'GET').content

  def to_pandas(self):
    """
    Returns all data in the dat as a pandas dataframe.
    """
    if not pandas:
      print "Could not find pandas in this environment. Do you have it installed?"
      return False

    return pandas.read_csv(self.api_base + '/csv')
