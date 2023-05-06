with open("output.txt") as f:
    n = int(f.readline().split()[-1])
    e = int(f.readline().split()[-1])
    encrypt = int(f.readline().split()[-1])
    r = int(f.readline().split()[-1])

# split p and q from r
pq = []
mask = int("55" * 128, 16)
pq.append(r & mask)
mask <<= 1
pq.append(r & mask)
if pq[0] > pq[1]:
    pq[0], pq[1] = pq[1], pq[0]

# recover p and q
for bit in range(0, 8 * 128 + 1):
    target = int(bit % 2 == 0)
    candidate = pq[target] + (1 << bit)
    mask = int("1" * (bit + 1), 2)
    n_sub = n & mask
    if (candidate * pq[target - 1]) & mask == n_sub:
        pq[target] = candidate
assert pq[0] * pq[1] == n

# decrypt
phi = (pq[0] - 1) * (pq[1] - 1)
d = pow(e, -1, phi)
plain = pow(encrypt, d, n)
print(plain.to_bytes(64, byteorder="big").decode())
