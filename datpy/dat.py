import subprocess
import time


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

