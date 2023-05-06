from pwn import remote
from math import gcd

q = 139595134938137125662213161156181357366667733392586047467709957620975239424132898952897224429799258317678109670496340581564934129688935033567814222358970953132902736791312678038626149091324686081666262178316573026988062772862825383991902447196467669508878604109723523126621328465807542441829202048500549865003
p = 2 * q + 1
g = 2
s = []
candidate = 0
while True:
    sock = remote("18.183.181.101", 50010)
    sock.recvline()
    sock.recvline()
    sock.recvline()
    sock.recvuntil(b"= ")
    y = int(sock.recvline().decode())
    sock.recvline()
    sock.recvuntil(b"= ")
    h = int(sock.recvline().decode(), 16)
    sock.recvuntil(b"= ")
    r = int(sock.recvline().decode())
    sock.recvuntil(b"= ")
    s_tmp = int(sock.recvline().decode())
    sock.close()
    s.append(s_tmp)
    for i in range(len(s) - 1):
        s_dif = max(s[i], s[-1]) - min(s[i], s[-1])
        s_dif = s_dif * pow(r, -1, q) % q
        if len(bin(s_dif)[2:]) < 650:
            if candidate == 0:
                candidate = s_dif
            else:
                candidate = gcd(candidate, s_dif)
    print(candidate)
    if b"FLAG" in candidate.to_bytes(32, "big"):
        print(candidate.to_bytes(32, "big"))
        break
