import subprocess
import time
import json

try:
  import pandas as pd
except:
  pd = False

class Dat:

  def __init__(self, location=None):
    if location:
      subprocess.call(["cd", self.location])
      self.location = location

    self.version = None

  def init(self):
    return subprocess.call(["dat init --no-prompt"], shell=True)

  def checkout(self, version):
    self.version = version
    return subprocess.call(["dat checkout " + version], shell=True)

  def import_file(self, filename, **kwargs):
    p = process("dat import " + filename, kwargs)
    stdout, stderr = p.communicate()
    return _set_version_from_log(stdout)

  def import_dataframe(self, dataframe, **kwargs):
    ## TODO: make streaming by using a generator
    p = process("dat import -", kwargs)
    stdout, stderr = stream_in(p, dataframe.to_csv(), parse=True)
    return _set_version_from_log(stdout)

  def write(self, name, data, **kwargs):
    p = process("dat write " + name + " -", kwargs)
    stdout, stderr = stream_in(p, data, parse=False)
    return _set_version_from_log(stdout)

  def write_file(self, filename, **kwargs):
    p = process("dat write " + filename, kwargs)
    stdout, stderr = p.communicate()
    return _set_version_from_log(stdout)

  def export_as_dataframe(self, dataset, **kwargs):
    if not pd:
      raise Exception("Can't find pandas. Is it available on your path?")

    output = self.export(dataset, **kwargs)
    return pd.DataFrame.from_dict(output)

  def cat(self, filename, **kwargs):
    return stream_out("dat cat " + filename, kwargs, parse=False)

  def export(self, dataset, **kwargs):
    return stream_out("dat export -d " + dataset, kwargs)

  def clean(self, **kwargs):
    return subprocess.call(["rm -rf .dat"], shell=True)

  def _set_version_from_log(self, stdout):
    log = json.loads(stdout)
    self.version = log["version"]
    return self.version

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

  opts['log'] = 'json'

  for key, val in opts.iteritems():
    if (len(key) == 1):
      cmd += ' -' + key + ' ' + val
    else:
      cmd += ' --' + key + '=' + val

  return subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

def stream_in(p, data, parse=True):
  """
  Streams to dat from the given command into python

  Parameters
  ----------
  cmd: str
    the command to execute
  parse: boolean
    TODO: if true, will try to parse the output from python generator or list

  """
  out = p.communicate(input=data)
  if p.returncode == 1:
    raise Exception(out[1])
  else:
    return out

def stream_out(cmd, opts=None, parse=True):
  """
  Streams the stdout from the given command into python

  Parameters
  ----------
  cmd: str
    the command to execute
  parse: boolean
    if true, will try to parse the output from json objects to
    python lists/dictionaries
  """
  p = process(cmd, opts)

  if parse:
    res = []
    for line in iter(p.stdout.readline, ''):
      parsed = json.loads(line.rstrip())
      res.append(parsed)
  else:
    res = ''
    for line in iter(p.stdout.readline, ''):
      res += line

  subprocess.Popen.terminate(p)
  return res
