#!/usr/bin/env python2

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def bfks(pubkey, bfrange):
    for n in xrange(1, bfrange):
        for m in xrange(1, bfrange):
            # compute a private key candidate given n & m
            priv = [(i*n)%m for i in pub]
            privs = sorted(priv)
            # check if the candidate key is sorted and 1st number is not 0
            if priv == privs and priv[0] != 0:
                superincreasing = 1
                sum = 0
                # check that the candidate key is superincreasing
                for i in priv:
                    if i <= sum:
                        superincreasing = 0
                    sum += i
                if superincreasing and pub == [(i*n)%m for i in priv]:
                    return priv, n, m
    return None, 0, 0

if __name__ == "__main__":
    
    pub  = [99, 1235, 865, 990, 5, 1443, 895, 1477]
    ct = "11b90d6311b90ff90ce610c4123b10c40ce60dfa123610610ce60d450d000ce61061106110c4098515340d4512361534098509270e5d09850e58123610c9"
    bfrange = 5000

    print "[*] Start bruteforcing private key\n"
    priv, n, m = bfks(pub, bfrange)
    if priv:
        print "[+] Priv key found: " + ', '.join(str(i) for i in priv)
        print "[+] n = " + str(n)
        print "[+] m = " + str(m)

        # split cipher text in strings of 4 chars (16 bit hex value)
        ct_dec = [int(h,16) for h in map(''.join, zip(*[iter(ct)]*4))]
        # decrypt
        n1 = modinv(n, m)
        pt_dec = [(i*n1)%m for i in ct_dec]

        # pre-compute values in priv key base
        dic = {}
        for i in range(0, pow(2,len(priv))):
            b = bin(i)[2:].zfill(8)[::-1]
            sum = 0
            for j in range(len(b)):
                if b[j] == '1':
                    sum += priv[j]
            dic[sum] = i

        # lookup plain value in pre-computed dic
        pt = ''
        for b in pt_dec:
            pt += chr(dic[b])
        print "\n[*] Decrypted data: " + pt
    else:
        print "[-] No priv key found, try to increase the bf range."