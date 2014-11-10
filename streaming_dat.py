import json
import requests
import csv

port = 'http://localhost:6461'

def get_dat():
# returns json about dat
    try:
        call = port + '/api'
        req = requests.get(call, stream=True)
        print(req.content)
    except:
        raise Exception("You are not connected to DAT. Please enter \'dat listen\' ")
    return get_dat
get_dat()         

def get_datastore():
# json representation of dat
    try:
        call = port + '/api/row'
        req = requests.get(call, stream=True)
        print(req.content)
    except:
        raise Exception("You are not connected to DAT. Please enter \'dat listen\' ")
    return get_datastore
get_datastore()   

def get_session():
    # get session info
    try:
        call = port + '/api/session'
        req = requests.get(call, stream=True)
        print(req.content)
    except:
        raise Exception("You are not connected to DAT. Please enter \'dat listen \' ")
    return get_session
get_session()

def get_changes():
    # get changes
    try:
        call = port + '/api/changes'
        req = requests.get(call, stream=True)
        print(req.content)
    except:
        raise Exception("You are not connected to DAT. Please enter \'dat listen\' ")
    return get_changes
get_changes()