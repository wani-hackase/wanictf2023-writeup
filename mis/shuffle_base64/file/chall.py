import random
import itertools
import base64
import hashlib


def make_shuffle_list(m):
    num = []
    for i in range(len(m) // 3):
        num.append(i)

    return list(itertools.permutations(num, len(m) // 3))


def make_str_blocks(m):
    tmp = ""
    ret = []
    for i in range(len(m)):
        tmp += m[i]
        if i % 3 == 2:
            ret.append(tmp)
            tmp = ""
    return ret


def pad(m):
    ret = ""
    for i in range(len(m)):
        ret += m[i]
        if i % 2:
            ret += chr(random.randrange(33, 126))

    while len(ret) % 3:
        ret += chr(random.randrange(33, 126))
    return ret


flag = "FAKE{DUMMY_FLAG}"
# FLAG check
# assert (hashlib.sha256(flag.encode()).hexdigest() == "19b0e576b3457edfd86be9087b5880b6d6fac8c40ebd3d1f57ca86130b230222")

padflag = pad(flag)
shuffle_list = make_shuffle_list(padflag)
str_blocks = make_str_blocks(padflag)
order = random.randrange(0, len(shuffle_list) - 1)
cipher = ""
for i in shuffle_list[order]:
    cipher += str_blocks[i]
cipher = base64.b64encode(cipher.encode())

print(f"cipher = {cipher}")
