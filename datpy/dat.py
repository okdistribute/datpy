import subprocess
import time
import json

def get_process(args, shell=True):
  return subprocess.Popen(args, stdout=subprocess.PIPE, shell=True)

class LocalDat:

  def __init__(self, location=None):
    if location:
      subprocess.call(["cd", self.location])
      self.location = location

  def call(self, args, shell=True):
    return subprocess.call(args, shell=shell)
  
  def init(self):
    return self.call(["dat init --no-prompt"])

  def add(self, filename):
    return self.call(["dat add " + filename])

  def heads(self):
    p = get_process("dat heads")
    return p.stdout.read()

  def cat(self):
    p = get_process("dat cat")
    res = []
    for line in iter(p.stdout.readline, ''):
      line = line.rstrip()
      try:
        parsed = json.loads(line)
        res.append(parsed)
      except:
        pass
             
    subprocess.Popen.terminate(p)
    return res

  def listen(self):
    p = get_process("dat listen")
    while p.stdout.read(1) == None:
      time.sleep(.5)
      
    self.server = p
    return self.server

  def close(self):
    return subprocess.Popen.terminate(self.server)

  def clean(self):
    return self.call(["rm -rf .dat"])

