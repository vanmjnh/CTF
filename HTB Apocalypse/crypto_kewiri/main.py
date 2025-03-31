
from sage.all import *
from pwn import remote

r = remote("83.136.250.155", 34917)
print(r.recvline().decode())

print(r.recvline().decode().strip())
print(r.recvuntil(b'p = ').decode().strip(), end=' ')
p = int(r.recvline().decode().strip())
print(p, '\n')

'''--------01--------'''
a1 = p.bit_length()
r.sendline(str(a1).encode())
print(r.recv().decode(), a1)
'''--------02--------'''
factors = [(2, 2), (5, 1),(635599, 1), (2533393, 1),(4122411947, 1), (175521834973, 1), (206740999513, 1), (1994957217983, 1), (215264178543783483824207, 1), (10254137552818335844980930258636403, 1)]
a2 = '2,2_5,1_635599,1_2533393,1_4122411947,1_175521834973,1_206740999513,1_1994957217983,1_215264178543783483824207,1_10254137552818335844980930258636403,1'
r.sendline(a2.encode())
print(r.recv().decode(), a2)
'''--------03--------'''
def is_primitive_root_fast(g, p, factors):
    for q in factors:
        if pow(g, (p-1) // q, p) == 1:
            return False
    return True

phi = p - 1
factors = [f[0] for f in factors]

for i in range(17):
    try:
        q3 = r.recvuntil(b'>').decode()
    except:
        break
    print(q3, end=' ')
    e = int(q3.split()[-2][:-1])
    a3 = '1' if is_primitive_root_fast(e, p, factors) == 1 else '0'
    print(a3)
    r.sendline(a3.encode())

    # print(r.recvline().decode())
'''--------04--------'''
q4 = r.recvuntil(b'>').decode().strip()
print(q4, end=' ')
a4 = p
print(a4)
r.sendline(str(a4).encode())
'''--------05--------'''
factors = [(2, 2), (7, 2), (p, 1), (2296163171090566549378609985715193912396821929882292947886890025295122370435191839352044293887595879123562797851002485690372901374381417938210071827839043175382685244226599901222328480132064138736290361668527861560801378793266019, 1)]
a5 = "_".join([f"{p},{e}" for (p,e) in factors])
q5 = r.recvuntil(b'>').decode()
print(q5, end=' ')
r.sendline(a5.encode())
print(a5)
'''--------06--------'''
from smart_attack import attack
Fp = GF(p)
a = 408179155510362278173926919850986501979230710105776636663982077437889191180248733396157541580929479690947601351140
b = 8133402404274856939573884604662224089841681915139687661374894548183248327840533912259514444213329514848143976390134
E = EllipticCurve(Fp, [a, b])
G_x = Fp(10754634945965100597587232538382698551598951191077578676469959354625325250805353921972302088503050119092675418338771)
G = E.lift_x(G_x)
q6 = r.recvuntil(b'>').decode()
print(q6, end=' ')
A_x = Fp(int(q6.split("A has x-coordinate:")[1].split("\n")[0]))
A = E.lift_x(A_x)
d = attack(G, A)
a6 = str(d)
r.sendline(a6.encode())
print(a6)
r.interactive()



