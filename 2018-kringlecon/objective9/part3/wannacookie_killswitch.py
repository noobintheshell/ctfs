#!/usr/bin/env python
import socket
import dns.resolver
import re
import zlib
        
def getKillSwitch(resolver, s, ds):
    # s = "1f8b080000000000040093e76762129765e2e1e6640f6361e7e202000cdd5c5c10000000"
    # 1f8b080000000000 is GZ header -> 16 chars to skip

    decdata = zlib.decompress(s.decode('hex'), 16).encode('hex')
    srvdata = getTXTRecord(resolver, '6B696C6C737769746368' + '.' + ds)
    ks = ''.join([chr(ord(a)^ord(b)) for a,b in zip(decdata.decode('hex'), srvdata.decode('hex'))])
    print "[+] KILL SWITCH: " + ks.encode()
    
def getTXTRecord(resolver, ds):
    txt = resolver.query(ds, "TXT").response.answer[0].to_text()
    txt = re.findall('TXT \"(.+?)\"', txt)[0]
    return txt


if __name__ == "__main__":

    ds = "erohetfanu.com"
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [socket.gethostbyname(ds)]

    # -------------------
    # Get the Kill Switch
    # -------------------
    S1 = "1f8b080000000000040093e76762129765e2e1e6640f6361e7e202000cdd5c5c10000000"
    getKillSwitch(resolver, S1, ds)