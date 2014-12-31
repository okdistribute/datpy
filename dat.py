from requests import Request, Session
import json
import csv

VALID_GET_PARAMS = ['limit', 'start', 'gt', 'lt', 'gte', 'lte', \
    'reverse', 'version', 'style', 'since', 'tail', 'live']


class Dat:

  def __init__(self, host, username=None, password=None):
    # strip trailing slash
    self.host = host.strip('/')
    self.api_base = '{}/api'.format(self.host)
    self.auth = (username, password)

  def _call(self, resource, method, data=None, opts=None, stream=False):
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

  def info(self):
    return self._call('', 'GET')

  def diff(self):
    return self._call('changes', 'GET')

  def session(self):
    return self._call('session', 'GET')

  def csv(self):
    return self._call('csv', 'GET')

  def rows(self):
    req = self._call('rows', 'GET')
    output = json.loads(req)
    return output['rows']
