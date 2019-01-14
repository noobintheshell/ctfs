#!/usr/bin/env python
import socket
import dns.resolver
import re
import struct
import binascii
import zlib
from Crypto.Cipher import AES
    
def getTXTRecord(resolver, ds):
    txt = resolver.query(ds, "TXT").response.answer[0].to_text()
    txt = re.findall('TXT \"(.+?)\"', txt)[0]
    return txt

def getFile(resolver, file, ds):
    f = open(file, 'wb')
    count = int(getTXTRecord(resolver, file.encode("hex") + '.' + ds))
    for i in range(count):
        f.write(getTXTRecord(resolver, str(i) + '.' + file.encode("hex") + ds).decode('hex'))
    f.close()

def downloadFiles(resolver, files, ds):
    for k,v in files.items():
        print '[+] Downloading ' + k +' : ' + v
        getFile(resolver, v, ds)

def decryptFile(iFile, key):
    suffix = ".wannacookie"
    blocksize = 16
    oFile = iFile[:-len(suffix)]
    
    with open(iFile, 'rb') as infile:
        print '[+] Decrypting ' + iFile
        
        ivlen = struct.unpack('=L',infile.read(4))[0]
        iv = infile.read(ivlen)

        decryptor = AES.new(key.decode('hex'), AES.MODE_CBC, iv)

        with open(oFile, 'wb') as outfile:
            while True:
                chunk = infile.read(blocksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))


if __name__ == "__main__":

    ds = "erohetfanu.com"
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [socket.gethostbyname(ds)]
    
    # -------------------------------------
    # Download files from ransomware server
    # -------------------------------------
    srvFiles = \
    {
        #"Pub Key": "server.crt",
        #"Priv Key": "server.key",
        #"Ransomware Source Min" : "wannacookie.min.ps1",
        #"Ransomware Source" : "wannacookie.ps1",
        #"Web Source Min":"source.min.html"
        "Web Source":"source.html"
    }
    downloadFiles(resolver, srvFiles, ds)

    # ----------------------
    # Decrypt Alabaster's DB
    # ----------------------
    encFile = "alabaster_passwords.elfdb.wannacookie"
    key = "fbcfc121915d99cc20a3d3d5d84f8308"
    #decryptFile(encFile, key)    