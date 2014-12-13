import unittest
import requests

port = 'http://localhost:6461'

def info():
    call = port + '/api'
    req = requests.get(call, stream=True)
    print(req.content)
    return req.status_code

class DatTest(unittest.TestCase):

    def test_info(self):
    	self.assertEqual(info(), 200)
        
if __name__ == '__main__':
    unittest.main()
