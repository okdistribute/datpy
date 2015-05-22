import subprocess
import time
import json

def stream_out(cmd, opts, parse=True):
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
  cmd = get_command(cmd, opts)
  p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

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

def get_command(cmd, opts):
  """
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

  for key, val in opts.iteritems():
    if (len(key) == 1):
      cmd += ' -' + key + ' ' + val
    else:
      cmd += ' --' + key + '=' + val

  return cmd

class Dat:

  def __init__(self, location=None):
    if location:
      subprocess.call(["cd", self.location])
      self.location = location

  def call(self, cmd, opts=None):
    cmd = get_command(cmd, opts)
    return subprocess.call(cmd, shell=True)

  def init(self):
    return self.call(["dat init --no-prompt"])

  def add(self, filename, **kwargs):
    cmd = "dat import " + filename
    return self.call(cmd, kwargs)

  def heads(self):
    res = stream_out("dat heads")
    return res

  def write(self, filename, **kwargs):
    return self.call("dat write " + filename, kwargs)

  def cat(self, filename, **kwargs):
    return stream_out("dat cat " + filename, kwargs, parse=False)

  def export(self, dataset, **kwargs):
    return stream_out("dat export -d " + dataset, kwargs)

  def close(self):
    return subprocess.Popen.terminate(self.server)

  def clean(self):
    return self.call(["rm -rf .dat"])

