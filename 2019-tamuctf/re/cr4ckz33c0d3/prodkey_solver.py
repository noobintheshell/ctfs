#!/usr/bin/env python2
import logging
logging.getLogger('angr').setLevel('ERROR')
import angr
from pwn import *

proj = angr.Project('./prodkey') # load our binary
# flag like xxxxx-xxxxx-xxxxx-xxxxx-xxxxx
flag_size = 29

initial_state = proj.factory.entry_state()

# add contraints - flag contains only printable chars
for _ in range(flag_size):
    k = initial_state.posix.files[0].read_from(1)
    initial_state.add_constraints(k >= 0x21)
    initial_state.add_constraints(k <= 0x7a)

# add constraint - last byte = '\n'
k = initial_state.posix.files[0].read_from(1)
initial_state.add_constraints(k == 10)

# reset symbolic stdin and set its length to flag size + 1 ('\n') 
initial_state.posix.files[0].seek(0)
initial_state.posix.files[0].length = flag_size+1

# initialize simulation manager
print("[*] Start angr explore...")
simgr = proj.factory.simulation_manager(initial_state)

# set exploring strategy to DFS
# https://docs.angr.io/core-concepts/pathgroups#exploration-techniques
simgr.use_technique(angr.exploration_techniques.DFS())
simgr.explore(find = 0x400e58) # explore the address of fopen('flag.txt', 'r') call

# a state that reached the find condition from explore
if simgr.found:
    found = simgr.found[0] 
    key = found.posix.dumps(0).replace('\x00', '') # strip all null bytes

    print("[+] Found key: " + key)

    # if a key is found we connect to tamuctf service and send the key to get the flag
    conn = remote('rev.tamuctf.com', 8189)
    print(conn.recvuntil('continue:', drop=False))
    print(key.rstrip('\n'))
    conn.sendline(key.rstrip('\n'))
    print(conn.recvuntil('}', drop=False))
else:
    print("[-] Key not found")