#!/usr/bin/env python3
from itertools import product
import math

def isPrime(n):
    ''' 
    https://www.geeksforgeeks.org/analysis-different-methods-find-prime-number-python/
    ''' 
    if n <= 1: 
        return False
    if n == 2: 
        return True
    if n > 2 and n % 2 == 0: 
        return False
  
    max_div = math.floor(math.sqrt(n)) 
    for i in range(3, 1 + max_div, 2): 
        if n % i == 0: 
            return False
    return True
  
numbers = ['1', '3', '7']
for n in product(numbers, repeat=4):
    p = int(''.join(n))
    if all(elem in n for elem in numbers) and isPrime(p):
        print(''.join(n))