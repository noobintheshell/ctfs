#!/usr/bin/env python3
from datetime import datetime, timezone
from Crypto.Cipher import DES

# try all timestamps on December 6, 2019, between 7pm and 9pm UTC
# 7200 tries in total
tstart = int(datetime(2019,12,6,19,0,0,tzinfo=timezone.utc).timestamp())
tend   = int(datetime(2019,12,6,21,0,0,tzinfo=timezone.utc).timestamp())

with open('ElfUResearchLabsSuperSledOMaticQuickStartGuideV1.2.pdf.enc', 'rb') as f:
    finbytes = f.read()

akey=[0]*8
for seed in range(tstart, tend+1):
    t = seed

    # compute DES key
    for i in range(len(akey)):
        t = t*0x343fd + 0x269ec3
        akey[i]=(t>>0x10&0x7fff)&0xff
    key = bytes(akey)

    # decrypt data
    des = DES.new(key, DES.MODE_CBC, bytes([0]*8)) # IV = 0
    foutbytes = des.decrypt(finbytes)

    # search for "%PDF" in decrypted data
    if b"\x25\x50\x44\x46" in foutbytes[0:4]:
        print("GOT IT with Seed = {0}".format(seed))
        with open('ElfUResearchLabsSuperSledOMaticQuickStartGuideV1.2.pdf', 'wb') as f:
            f.write(foutbytes)
        exit()