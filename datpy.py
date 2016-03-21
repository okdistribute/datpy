from __future__ import absolute_import
from __future__ import unicode_literals
from pkg_resources import parse_version

import pickle
import os
import subprocess
import time

try:
  import ujson as json
except:
  import json


COMPATIBLE_DAT_VERSION = '9.8.2'

class DatException(Exception):
  pass

def on_error(log):
  message = log.get('message')
  if not message:
    message = 'Unknown error. Please contact us at #dat in freenode on irc'
  raise DatException('Error: ' + message)

class Dat(object):

  def __init__(self, home=None):
    self.home = home
    self._opened = []

  def close(self, pid=None):
    for p in self._opened:
      if not pid:
        subprocess.Popen.terminate(p)
      if pid == p.pid:
        subprocess.Popen.terminate(p)
    return True

  def link(self, path):
    res = []
    p = self._call('link {0}'.format(path))
    for line in iter(p.stdout.readline, b''):
      res.append(line)
      line = line.decode()
      index = line.find('dat://')
      if index > -1:
        self._opened.append(p)
        link = line[index:].strip()
        return link

    for line in iter(p.stderr.readline, b''):
      res.append(line)

    raise Exception(''.join(res))

  def download(self, link, path=None):
    opts = {}
    if path:
      opts['path'] = path
    p = self._call(link, opts)
    self._opened.append(p)
    for line in iter(p.stdout.readline, b''):
      line = line.decode()
      if line.find('Downloaded to') > -1:
        return True
    return False

  def _call(self, cmd, opts=None):
    if opts is None:
      opts = {}
    if self.home:
      opts['home'] = self.home
    return process(cmd, opts)

def process(cmd, opts):
  """
  Creates a process.
  Adds options (provided as keyword args) to the given cmd.

  Parameters
  ----------
  cmd: str
    the command to add options
  opts: dict
    the options to add
  """
  if opts is None:
    opts = {}

  cmd = 'dat ' + cmd + ' -q'

  for key, val in opts.items():
    if (len(key) == 1):
      cmd += " -{0} {1}".format(key, val)
    else:
      cmd += " --{0}={1}".format(key, val)

  current_version = subprocess.check_output(['dat -v'], shell=True).decode().strip()
  if parse_version(current_version) < parse_version(COMPATIBLE_DAT_VERSION):
    raise DatException("Please update the dat version with npm install -g dat.",
                    "Your version is {0}, this datpy requires {1}".format(current_version, COMPATIBLE_DAT_VERSION))
  return subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                          stderr=subprocess.PIPE, shell=True)

def stream_in(p, data):
  """
  Streams to dat from the given command into python

  Parameters
  ----------
  cmd: str
    the command to execute
  parse: boolean
    TODO: if true, will try to parse the output from python generator or list

  """
  if isinstance(data, str):
    data = data.encode()
  stdout, stderr = p.communicate(input=data)
  if p.returncode == 1:
    raise DatException('Node.js error: ' + stderr)
  elif p.returncode == 127:
    raise DatException("It looks like `dat` commandline is missing from PATH.\n",
                   "Are you sure you installed it?\n"
                   "Check http://dat-data.com for instructions")
  else:
    try:
      res = json.loads(stdout.decode())
      if type(res) == dict and res.get('error'):
        return on_error(res)
    except ValueError:
      res = {'stdout': stdout, 'stderr': stderr}

    return res

def stream_out(p, parse=True):
  """
  Streams the stdout from the given command into python

  Parameters
  ----------
  cmd: str
    the command to execute
  parse: boolean
    to parse the file into json
  """
  res = []
  for line in iter(p.stdout.readline, b''):
    try:
      line = line.decode()
      if parse:
        line = json.loads(line.rstrip())
    except UnicodeDecodeError:
      line = pickle.loads(line)
      parse = True
    res.append(line)

  if len(res) == 1:
    res = res[0]
    if type(res) == dict and res.get('error'):
      return on_error(res)

  if not parse:
    res = ''.join(res)

  subprocess.Popen.terminate(p)
  return res
