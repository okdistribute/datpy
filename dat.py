from requests import Request, Session
import json
import csv
import subprocess

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
    self.server = subprocess.Popen("dat listen", shell=True)
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
    res_type = opts.get('type')
    if res_type:
        if res_type == 'csv':
            headers['content-type'] = 'text/csv'
        elif res_type == 'json':
            headers['content-type'] = 'application/json'

    req = Request(method, url, params=params, data=data, headers=headers)

    s = Session()
    if self.auth:
        s.auth = self.auth

    prepped = s.prepare_request(req)
    resp = s.send(prepped, stream=stream)
    return resp.content

  def json(self, *args, **kwargs):
    resp = self.api(*args, **kwargs)
    return json.loads(resp)

  def info(self):
    return self.json('', 'GET')

  def changes(self):
    resp = self.json('changes', 'GET')
    return resp['rows']

  def session(self):
    return self.json('session', 'GET')

  def csv(self):
    return self.api('csv', 'GET')

  def rows(self):
    resp = self.json('rows', 'GET')
    return resp['rows']
