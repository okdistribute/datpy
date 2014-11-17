import requests
import json

class Dat:
    def __init__(self, host):
        req = requests.get(host, stream=True)
        self.host = host
        #self.session = requests.get(host, stream=True)  

    def dat_info(host):
        call = str(host + '/api')
        return dat_info
        print (req.content)
    
    
    def dat_diff(host):
        call = host + '/api/changes'
        return dat_info
        print (req.content)

