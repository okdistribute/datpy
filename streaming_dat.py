import json
import requests

port = 'http://localhost:6461'

def get_dat():
    try:
        call = port + '/api'
        req = requests.get(call, stream=True)
        print(req.content)
    except:
        raise Exception("You are not Connected to DAT. Please enter \'dat listen\' ")
    return get_dat
get_dat()         

def get_datastore():
    try:
        call = port + '/api/rows'
        req = requests.get(call, stream=True)
        print(req.content)
    except:
        raise Exception("You are not connected to DAT. Please enter \'dat listen\' ")
    return get_datastore
get_datastore()
