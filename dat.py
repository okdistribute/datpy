from requests import Request, Session
import json
import csv
import subprocess
import time

VALID_GET_PARAMS = ['limit', 'start', 'gt', 'lt', 'gte', 'lte', \
    'reverse', 'version', 'style', 'since', 'tail', 'live', 'type']

class DatServerError(Exception):
  def __init__(self, resp):
    self.resp = resp
    self.resp_content = json.loads(resp.content)

    if self.resp_content.get('conflict'):
      message = self.resp_content['error']
    else:
      message = "Unknown server error. Received status code %s" % (self.status)
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

    if not data:
      data = {}
    if not opts:
      opts = {}

    params = {}
    for param in VALID_GET_PARAMS:
      if opts.get(param):
        params[param] = opts[param]

    headers = {}
    data_format = opts.get('type')
    if not data_format:
      data_format = 'json' if type(data) == dict else 'csv'

    if data_format == 'csv':
        headers['content-type'] = 'text/csv'
    elif data_format == 'json':
        headers['content-type'] = 'application/json'
        data = json.dumps(data)

    req = Request(method, url, params=params, data=data, headers=headers)

    s = Session()
    if self.auth:
        s.auth = self.auth

    prepped = s.prepare_request(req)
    resp = s.send(prepped, stream=stream)
    if resp.status_code == 200 or resp.status_code == 201:
      return resp.content
    raise DatServerError(resp)

  def json(self, *args, **kwargs):
    resp = self.api(*args, **kwargs)
    return json.loads(resp)

  def info(self):
    return self.json('', 'GET')

  def changes(self, opts=None):
    resp = self.json('changes', 'GET', opts=opts)
    return resp['rows']

  def session(self):
    return self.json('session', 'GET')

  def csv(self):
    return self.api('csv', 'GET')

  def rows(self, opts=None):
    resp = self.json('rows', 'GET', opts=opts)
    return resp['rows']

  def put(self, data, opts=None):
    return self.json('rows', 'POST', data=data, opts=opts)


