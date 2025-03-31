from pwn import remote, process
import string

# r = process(['python3', 'server.py'])
r = remote("94.237.48.197", 42489)

def send_user(user):
    r.recvuntil(b'::').decode()
    r.sendline(b'1')
    r.recvuntil(b'::').decode()
    r.sendline(user)

chars = string.ascii_letters+string.digits
length = 20 # length target
size = length + (16 - (length % 16)) % 16
assert size > 16
iv_ctrlBlock = '_'*size
feedback_targetBlock = '_'*size

target = ''
i = 1
while i <= length:
    for char in chars:
        payload = iv_ctrlBlock[-(size-1):] + char + feedback_targetBlock[-(size-i):]
        print(iv_ctrlBlock[-(size-1):] + char + iv_ctrlBlock[-(size-1):] + '?')
        send_user(payload.encode())
        recv = r.recvline().decode()
        ct = recv.strip().split(': ')[-1]
        ctBlock = [ct[i:i+32] for i in range(0, len(ct), 32)]
        position = size//16
        if ctBlock[position-1] == ctBlock[2*position-1]:
            i += 1
            target += char
            iv_ctrlBlock += char    
            break
    else:
        break
print(target)
r.interactive()

# HTB{encrypting_with_CBC_decryption_is_as_insecure_as_ECB___they_also_both_fail_the_penguin_test_45a51d2e0f355c58b258a00894cf8a16}
# HTB{encrypting_with_CBC_decryption_is_as_insecure_as_ECB___they_also_both_fail_the_penguin_test_783eed6404bb68686a7643c4a8f9f604}