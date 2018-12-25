#!/usr/bin/env python
import functools
import re
import itertools
import string
import hashlib
from crypto_commons.netcat.netcat_commons import nc, receive_until_match, send

def captcha (s):
    for w in itertools.product(string.ascii_lowercase+string.ascii_uppercase, repeat=5):
        if hashlib.md5(''.join(w)).hexdigest()[:5] == s:
            passwd = ''.join(w)
            return passwd

# Code from https://en.wikipedia.org/wiki/Nim
def nim(heaps, game_type):

    #print(game_type, heaps)

    is_misere = game_type == 'misere'

    is_near_endgame = False
    count_non_0_1 = sum(1 for x in heaps if x > 1)
    is_near_endgame = (count_non_0_1 <= 1)

    # nim sum will give the correct end-game move for normal play but
    # misere requires the last move be forced onto the opponent
    if is_misere and is_near_endgame:
        moves_left = sum(1 for x in heaps if x > 0)
        is_odd = (moves_left % 2 == 1)
        sizeof_max = max(heaps)
        index_of_max = heaps.index(sizeof_max)

        if sizeof_max == 1 and is_odd:
            return "You will lose :("

        # reduce the game to an odd number of 1's
        return index_of_max, sizeof_max - int(is_odd)

    nim_sum = functools.reduce(lambda x, y: x ^ y, heaps)
    if nim_sum == 0:
        return "You will lose :("

    # Calc which move to make
    for index, heap in enumerate(heaps):
        target_size = heap ^ nim_sum
        if target_size < heap:
            amount_to_remove = heap - target_size
            return index, amount_to_remove


HOST = '199.247.6.180'
PORT = 14002;

if __name__ == "__main__":

    s = nc(HOST, PORT)

    # pass CAPTCHA
    r = s.recv(4096)
    md5_s = re.findall('md5\(X\).hexdigest\(\)\[\:5\]=(.+?)\.', r)[0]
    send(s, captcha(md5_s))

    # start NIM game
    r = receive_until_match(s, 'Input the pile:')
    state = map(int, re.findall('Current state of the game: \[(.*)\]', r)[0].split(','))

    while(True):
        print 'STATE: ' + str(state)
        index, quantity = nim(state, 'normal')
        print 'SEND: index = ' + str(index) + ', quantity = ' + str(quantity)
        send(s, str(index))
        send(s, str(quantity))

        if(state.count(0) != 14):
            r = receive_until_match(s, 'Input the pile:')
            state = map(int, re.findall('Current state of the game: \[(.*)\]', r)[1].split(','))
        else:
            break
    
    r = receive_until_match(s, '}')
    print r