#!/usr/bin/env python

def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
        gcd = b
    return gcd, x, y

q = 509
p = 4973
e = 43
n = p*q
cts = [906851,991083,1780304,2380434,438490,356019,921472,822283,817856,556932,2102538,2501908,2211404,991083,1562919,38268]
phi = (p - 1) * (q - 1)
gcd, d, b = egcd(e, phi)

pts = [] 
for ct in cts:
    pt = pow(ct, d, n)
    print pt
    if pt <=126:
        pts.append(pt)
    elif str(pt)[0] == '1':
        pts.append(int(str(pt)[:3]))
        pts.append(int(str(pt)[3:]))
    else:
        pts.append(int(str(pt)[:2]))
        pts.append(int(str(pt)[2:]))

print ''.join([chr(i) for i in pts])