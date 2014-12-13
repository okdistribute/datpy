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

def diff():
    call = port + '/api/changes'
    req = requests.get(call, stream=True)
    print(req.content)
    return req.headers['content-type']

def post_json():
	def post_file(filename):
    call = port + '/api/rows/post'
    with open(filename, 'rb') as f:
        req = requests.post(call, data=f)
    print(req.headers)
    return req.headers['content-type']


class DatTest(unittest.TestCase):

    def test_info(self):
    	self.assertEqual(info(), 200)

    def test_rows(self):
    	self.assertEqual(rows(),'application/json')

    def test_diff(self):
    	self.assertEqual(diff(),'application/json')

    def test_post_json(self):
    	self.assertEqual(test_post_json(), 'application/json')



        
if __name__ == '__main__':
    unittest.main()
