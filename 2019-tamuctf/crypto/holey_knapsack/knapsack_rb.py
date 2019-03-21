#!/usr/bin/env python2

pub  = [99, 1235, 865, 990, 5, 1443, 895, 1477]
ct = "11b90d6311b90ff90ce610c4123b10c40ce60dfa123610610ce60d450d000ce61061106110c4098515340d4512361534098509270e5d09850e58123610c9"
pt = ''

# pre-compute values in pub key base
dic = {}
for i in range(0, pow(2,len(pub))):
    b = bin(i)[2:].zfill(8)[::-1]
    sum = 0
    for j in range(8):
        if b[j] == '1':
            sum += pub[j]
    dic[sum] = i

# split cipher text in strings of 4 chars (16 bit hex value)
ct_dec = [int(h,16) for h in map(''.join, zip(*[iter(ct)]*4))]
# lookup value in pre-computed dic
for i in ct_dec:
    pt += chr(dic[i])
print pt