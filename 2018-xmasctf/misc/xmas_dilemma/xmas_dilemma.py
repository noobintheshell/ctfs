#!/usr/bin/env python
import hashlib;
import re
import itertools
import string
from numpy import arange
from crypto_commons.netcat.netcat_commons import nc, receive_until_match, send
import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline
import matplotlib.pyplot as plt

HOST = '199.247.6.180'
PORT = 14001;

def captcha (s):
    for w in itertools.product(string.ascii_lowercase+string.ascii_uppercase, repeat=5):
        if hashlib.md5(''.join(w)).hexdigest()[:5] == s:
            passwd = ''.join(w)
            return passwd

def query(s, x):
    send(s, '1')
    send(s, str(x))
    r = receive_until_match(s, 'Guess the global maximum')
    y = float(re.findall('f\(.*\) = (.*)', r)[0])
    print "Y = " + str(y)
    return y

def guess(s, y):
    send(s, '2')
    send(s, str(y))
    return receive_until_match(s, 'Guess the global maximum')

if __name__ == "__main__":

    s = nc(HOST, PORT)

    # pass CAPTCHA
    r = s.recv(4096)
    md5_s = re.findall('md5\(X\).hexdigest\(\)\[\:5\]=(.+?)\.', r)[0]
    send(s, captcha(md5_s))

    # start retrieving information
    r = receive_until_match(s, 'Guess the global maximum')

    # getting x range
    x_range = re.findall('defined in range \((.*), (.*)\)', r)
    x_min = float(x_range[0][0])
    x_max = float(x_range[0][1])

    # getting f(x) values
    j=0
    x = []
    y = []
    for i in arange(x_min, x_max, 0.4):
        x.append(i)
        y.append(query(s, i))
        j+=1
        if (j == 500):
            break

    # Code from https://stackoverflow.com/questions/50371298/find-maximum-minimum-of-a-1d-interpolated-function
    xa = np.array(x)
    ya = np.array(y)
    f = InterpolatedUnivariateSpline(xa, ya, k=4)
    cr_pts = f.derivative().roots()
    cr_pts = np.append(cr_pts, (xa[0], xa[-1]))  # also check the endpoints of the interval
    print cr_pts
    cr_vals = f(cr_pts)
    max_index = np.argmax(cr_vals)
    print "Maximum value at [" + str(cr_pts[max_index]) + ", " + str(cr_vals[max_index]) + "]"
    print "in range " + str(x_range)

    # start guessing value (~50% chances)
    res = round(cr_vals[max_index],2)
    for g in xrange(500-j):
        r = guess(s, res)
        if ('X-MAS{' in r):
            print r
            break
        res += 0.01

    s.close()

    # show function graph
    plt.plot(xa, ya, 'o', x, f(xa), '-')
    plt.show()