import json
import requests

r = requests.get('http://localhost:6461/api', stream=True)

print r.content

