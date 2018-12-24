#!/usr/bin/env python

# Code based on 
# https://github.com/ctf-x/ctfx-problems-2016/blob/master/crypto/little_crypto_gambler-150/gamble_solution.py

from fractions import gcd

def xgcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = xgcd(b % a, a)
        return (g, x - (b // a) * y, y)

def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)

def solve(s):
    nrand = len(s)
    t = []
    for x in range(nrand-1):
        t.append(s[x+1]-s[x])
    u = []
    for x in range(nrand-3):
        u.append(abs(t[x+2]*t[x]-t[x+1]**2))
    m = reduce(gcd, u)
    r4 = s[-4]
    r3 = s[-3]
    r2 = s[-2]
    r1 = s[-1]
    x = r2-r4
    b = r1-r3
    if x<0:
        x*=-1
        b*=-1
    if b<0:
        b=b%m
    g,x2,y2 = xgcd(x, m)
    if g==1:
        xi = x2%m
        a=(b*xi)%m
        c=(r1-r2*a)%m
        return [m,a,c]
    else:
        return None

# gather the first values of the series
s = [21462, 16214, 38352, 5582, 16424, 26348, 41005, 28554]

for i in range(20):
    m,a,c = solve(s)
    nextNum = (a*s[-1]+c)%m
    s.append(nextNum)
    print nextNum