import json
import requests

port = 'http://localhost:6461'

def get_dat():
# returns json about dat
    try:
        call = port + '/api'
        req = requests.get(call, stream=True)
        print(req.content)
    except:
        raise Exception("You are not Connected to DAT. Please enter \'dat listen\' ")
    return get_dat
get_dat()         

def get_datastore():
# json representation of dat
	try:
		call = port + '/api/row'
        req = requests.get(call, stream=True)
        print(req.content)
    except:
        raise Exception("You are not Connected to DAT. Please enter \'dat listen\' ")
    return get_datastore
get_datastore()   

      