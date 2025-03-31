# from pwn import *

# r = remote("83.136.252.198", 54240)

# print(r.recv().decode())

# r.sendline(b'join #general')


# with open("traces.txt", 'w') as f:
#     for i in range(21):
#         print(f.write(r.recvline().decode()))
from pwn import xor
import string

chars = string.printable[:-5]

with open("db.txt", 'r') as f:
    db = f.read()

def splitDB(db):
    db = db.strip()

    result = []
    for line in db.split('\n'):
        result.append(line.split(' : ')[1])
    
    return result

msg_list = splitDB(db)
msg_list = [bytes.fromhex(msg) for msg in msg_list]

while False:
    guess = input("Nhap guess: ")
    i = int(input("Nhap i: "))
    keyStream = xor(guess.encode(), msg_list[i])[:len(guess)]
    for j in range(len(msg_list)):
        print("[{:02d}]".format(j), xor(msg_list[j], keyStream)[:len(keyStream)])
# Here is the passphrase for our secure channel: %mi2gvHHCV5f_kcb=Z4vULqoYJ&oR
# )7

# -------------------------------secret--------------------------------------------------------------------------------------
with open("db1.txt", 'r') as f:
    db = f.read()

def splitDB(db):
    db = db.strip()

    result = []
    for line in db.split('\n'):
        result.append(line.split(' : ')[1])
    
    return result

msg_list = splitDB(db)
msg_list = [bytes.fromhex(msg) for msg in msg_list]

while False:
    guess = input("Nhap guess: ")
    i = int(input("Nhap i: "))
    if i < 0:
        for char in chars:
            tmp = guess + char
            keyStream = xor(tmp.encode(), msg_list[abs(i)])[:len(tmp)]
            for j in range(len(msg_list)):
                print("[{:02d}]".format(j), xor(msg_list[j], keyStream)[:len(keyStream)])
            choice = input("y/n: ")
            if choice == "y":
                guess += char
                break
    keyStream = xor(guess.encode(), msg_list[abs(i)])[:len(guess)]
    for j in range(len(msg_list)):
        print("[{:02d}]".format(j), xor(msg_list[j], keyStream)[:len(keyStream)])

# Yes, but we must treat it only as a last resort. If we activate it too soon, we risk revealing its location. It is labeled as: HTB{Crib_Dragging_Exploitation_With_Key_Nonce_Reuse!}
# 9



