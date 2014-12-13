import unittest
import requests

port = 'http://localhost:6461'

def info():
    call = port + '/api'
    req = requests.get(call, stream=True)
    print(req.content)
    return req.status_code

def rows():
    call = port + '/api/rows'
    req = requests.get(call, stream=True)
    print(req.content)
    return req.headers['content-type']

class DatTest(unittest.TestCase):

    def test_info(self):
    	self.assertEqual(info(), 200)

    def test_rows(self):
    	self.assertEqual(rows(),'application/json')


        
if __name__ == '__main__':
    unittest.main()
