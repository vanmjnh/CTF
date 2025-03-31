
from random import shuffle
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

n = 0x1337
e = 0x10001

def scramble(b, msg):
    return [msg[b[i]] for i in range(n)]

def super_scramble(msg, e):
    b = list(range(n))
    while e:
        if e & 1:
            b = scramble(b, msg)
        msg = scramble(msg, msg)
        e >>= 1
    return b

import ast

with open('tales.txt') as f:
    data = f.read()

scrambled_message = ast.literal_eval(data.split('scrambled_message = ')[1].split('\n')[0])
enc_flag = data.split('enc_flag = ')[1].strip().strip("'").strip('"')

from math import lcm

def permutation_cycles(p):
    seen = set()
    cycles = []
    for i in range(len(p)):
        if i not in seen:
            cycle = []
            j = i
            while j not in seen:
                seen.add(j)
                cycle.append(j)
                j = p[j]
            if len(cycle) > 1:
                cycles.append(cycle)
    return cycles

def permutation_order(p):
    cycles = permutation_cycles(p)
    lengths = [len(c) for c in cycles]
    if not lengths:
        return 1
    return lcm(*lengths)

from sympy import mod_inverse

order = permutation_order(scrambled_message)
try:
    d = mod_inverse(e, order)
except:
    print("Không tính được nghịch đảo modular")
    exit()

def permutation_pow(p, exp):
    res = list(range(len(p)))  # hoán vị đồng nhất
    base = p[:]
    while exp:
        if exp & 1:
            res = scramble(res, base)
        base = scramble(base, base)
        exp >>= 1
    return res

message = permutation_pow(scrambled_message, d)

from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import binascii

key = sha256(str(message).encode()).digest()
cipher = AES.new(key, AES.MODE_ECB)
flag_bytes = cipher.decrypt(bytes.fromhex(enc_flag))
try:
    flag = unpad(flag_bytes, 16)
except:
    flag = flag_bytes  # nếu không padding được thì in tạm

print(flag.decode(errors='ignore'))