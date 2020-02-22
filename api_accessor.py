import urllib.request
import json
import sys

key = sys.argv[1]
myurl = "https://0ron82vqjh.execute-api.us-east-2.amazonaws.com/posting/access-lambda?key="+key

req = urllib.request.Request(myurl)
req.add_header('Content-Type', 'application/json')
response = urllib.request.urlopen(req)
print(response.read())