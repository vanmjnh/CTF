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

message = list(range(n))
shuffle(message)

scrambled_message = super_scramble(message, e)

flag = pad(open('flag.txt', 'rb').read(), 16)

key = sha256(str(message).encode()).digest()
enc_flag = AES.new(key, AES.MODE_ECB).encrypt(flag).hex()

with open('tales.txt', 'w') as f:
    f.write(f'{scrambled_message = }\n')
    f.write(f'{enc_flag = }')