from __future__ import absolute_import
from __future__ import unicode_literals
from pkg_resources import parse_version

import pickle
import subprocess
import time

try:
  import ujson as json
except:
  import json

try:
  import pandas as pd
except:
  pd = False


COMPATIBLE_DAT_VERSION = '7.1.0'

class DatException(Exception):
  pass

def on_error(log):
  message = log.get('message')
  if not message:
    message = 'Unknown error. Please contact us at #dat in freenode on irc'
  raise DatException('Error: ' + message)

def returns_version(func):
  def inner(*args, **kwargs):
    self = args[0]
    log = func(*args, **kwargs)
    self.version = log.get("version")
    if not self.version:
      on_error(log)
    return self.version

  return inner

def clone(URL, path=None, **kwargs):
  """
  Parameters
  """
  if not path:
    path = ''
  p = process("dat clone {0} {1}".format(URL, path), kwargs)
  out = stream_out(p)
  return Dat(path)


class Dat(object):

  def __init__(self, path=None):
    self.path = path
    self.version = None

  def init(self, **kwargs):
    p = self.process("dat init --no-prompt", kwargs)
    return stream_out(p)

  def checkout(self, version, **kwargs):
    self.version = version
    p = self.process("dat checkout " + version, kwargs)
    return stream_out(p)

  def datasets(self, **kwargs):
    p = self.process("dat datasets", kwargs)
    res = stream_out(p)
    return res['datasets']

  def destroy(self, **kwargs):
    p = self.process("dat destroy --no-prompt", kwargs)
    return stream_out(p)

  def status(self, **kwargs):
    p = self.process("dat status", kwargs)
    return stream_out(p)

  def read(self, key, **kwargs):
    p = self.process("dat read " + key, kwargs)
    return stream_out(p, parse=False)

  @returns_version
  def write(self, filename, data=None, **kwargs):
    p = self.process("dat write {0} -".format(filename), kwargs)
    return stream_in(p, data)

  @returns_version
  def write_file(self, filename, **kwargs):
    p = self.process("dat write " + filename, kwargs)
    return stream_out(p)

  def process(self, cmd, opts):
    if self.path:
      opts['path'] = self.path

    return process(cmd, opts)

  def dataset(self, name):
    return Dataset(self, name)

class Dataset(object):

  def __init__(self, dat, dataset, key=False):
    self.dat = dat
    self.dataset = dataset
    self.key = key
    if not self.key:
      self.key = 'key'

  def keys(self, **kwargs):
    p = self.process("dat keys", kwargs)
    res = stream_out(p)
    if 'keys' in res:
      return res['keys']
    return res

  @returns_version
  def import_file(self, filename, **kwargs):
    p = self.process("dat import " + filename, kwargs)
    return stream_out(p)

  @returns_version
  def import_dataframe(self, dataframe, **kwargs):
    ## TODO: make streaming better by using a generator
    key = kwargs.get('key')
    if key:
      self.key = key
    p = self.process("dat import -", kwargs)
    return stream_in(p, dataframe.to_csv())

  def export_dataframe(self, **kwargs):
    if not pd:
      raise Exception("Can't find pandas. Is it available on your path?")

    output = self.export(**kwargs)
    frame = pd.DataFrame.from_dict(output)
    return frame

  def export(self, **kwargs):
    kwargs['full'] = True
    p = self.process("dat export", kwargs)
    output = stream_out(p)
    res = []
    for row in output:
      row['value'][self.key] = row['key']
      res.append(row['value'])
    return res

  def process(self, cmd, opts):
    if self.dat.path:
      opts['path'] = self.dat.path

    opts['dataset'] = self.dataset

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

  cmd += ' --json '

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
