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
        return req.content

    def diff(self):
        call = '{}/changes'.format(self.api_base)
        req = requests.get(call, stream=True)
        print(req.content)
        return req.content

    def session(self):
        call = '{}/session'.format(self.api_base)
        req = requests.get(call, stream=True)
        print(req.content)
        return req.content

    def csv(self):
        call = '{}/csv'.format(self.api_base)
        req = requests.get(call, stream=True)
        print(req.content)
        return req.content

    def rows(self):
        call = '{}/rows'.format(self.api_base)
        req = requests.get(call, stream=True)
        print(req.content)
        return req.content

    def dic(self):
        call = '{}/rows'.format(self.api_base)
        req = requests.get(call, stream=True)
        dat_dic = json.loads(req.text)
        print dat_dic
        return req.content

    def post_json(self, filename):
        call = '{}/rows'.format(self.api_base)
        with open(filename, 'rb') as f:
            req = requests.post(call, data=f)
        print(req.content)
        return req.content
        
    def post_csv(self, filename):
        call = '{}/bulk?results=true'.format(self.api_base)
        headers = {
        'content-type': 'text/csv',
        }
        with open(filename) as f:
            req = requests.post(call, data=f, headers=headers)
        print(req.content)
        return req.content
