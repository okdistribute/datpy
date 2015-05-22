import subprocess
import time
import json

def stream_in(cmd, data, opts=None, parse=True):
  """
  Streams to dat from the given command into python

  Parameters
  ----------
  cmd: str
    the command to execute
  parse: boolean
    if true, will try to parse the output from python generator or list
  """
  cmd = get_command(cmd, opts)
  p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

  if parse:
    count = 0
    for row in data:
      count += 1
      try:
        line = json.dumps(row)
      except:
        line = row

      p.stdin.write(line)
      p.stdin.write('\n')

    p.communicate()
  else:
    out = p.communicate(input=data)

  print count
  if p.returncode == 1:
    raise Exception(out[1])
  else:
    return 0

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
  cmd = get_command(cmd, opts)
  p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

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

def generator(df):
  cols = df.columns
  count = 0
  for kv in df.iterrows():
    row = kv[1]
    res = {}
    count += 1
    for i in xrange(0, len(cols)):
      col = cols[i]
      res[col] = row[i]
    yield res
  print count

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

  def import_from_file(self, filename, **kwargs):
    return self.call("dat import " + filename, kwargs)

  def import_from_pandas(self, dataframe, **kwargs):
    return stream_in("dat import -", generator(dataframe), kwargs, parse=True)

  def write(self, name, data, **kwargs):
    return stream_in("dat write " + name + " -", data, kwargs, parse=False)

  def write_from_file(self, filename, **kwargs):
    return self.call("dat write " + filename, kwargs)

  def cat(self, filename, **kwargs):
    return stream_out("dat cat " + filename, kwargs, parse=False)

  def export(self, dataset, **kwargs):
    return stream_out("dat export -d " + dataset, kwargs)

  def clean(self):
    return self.call(["rm -rf .dat"])

