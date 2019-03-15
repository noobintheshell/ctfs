#!/usr/bin/env python
from itertools import permutations

f = open('wordlist.txt', 'r')
lines = f.readlines()
f.close()

with open('wordlist_expanded.txt', 'w') as f:
    # combine up to 3 words
    for i in range(1,4):
        for group in permutations([c.strip('\n') for c in lines], i):
            f.write(''.join(group) + '\n')
            # append and prepend number from 0 to 9999
            for n in range(10000):
                f.write(''.join(group) + str(n) + '\n')
                f.write(str(n) + ''.join(group) + '\n')