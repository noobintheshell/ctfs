#!/usr/bin/env python2
import string
from pwn import * 

def enc(s):
    l = len(s)
    c = 0x48
    ct = ""
    for i in range(l):
        tmp = c * (ord(s[i]) + 0xc) + 0x11
        ct+= chr((tmp - ((((tmp * 0xea0ea0eb)>>32) >> 6) - (tmp >> 0x1f)) * 0x46) + 0x30)
        c = ord(ct[i])
    return ct

if __name__ == "__main__":
    assert(enc('abcdefghij\n') == 'IsZA<s<_2Us')
    
    encflag = '[OIonU2_<__nK<KsK'
    key = ''

    # bruteforce chars
    for i in range(len(encflag)-1):
        for c in string.printable:
            if enc(key + c + '\n')[:i+1] == encflag[:i+1]:
                key += c
                break
    print("Key: " + key) 

    # connect to tamuctf service
    conn = remote('rev.tamuctf.com', 7223)
    print(conn.recvuntil('continue:', drop=False))
    print(key.rstrip('\n'))
    conn.sendline(key.rstrip('\n'))
    print(conn.recvuntil('}', drop=False))