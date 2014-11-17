import requests
import json

class Dat:
    def __init__(self, host):
        self.req = requests.get(host, stream=True)
        self.host = host
        self.api_base = '{}/api'.format(self.host)

    def info(self):
        req = requests.get(self.api_base, stream=True)
        print(req.content)


