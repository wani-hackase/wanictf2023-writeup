import base64
from itertools import permutations
import hashlib

cipher = b"fWQobGVxRkxUZmZ8NjQsaHUhe3NAQUch"
cipher = base64.b64decode(cipher)

tmp1 = ""
for i in range(len(cipher)):
    if i % 3 == 2:
        continue
    tmp1 += chr(cipher[i])

blocks = []
tmp2 = ""
for i in range(len(tmp1)):
    tmp2 += tmp1[i]
    if i % 2:
        if "}" in tmp2:
            tmp2 = "}"
        blocks.append(tmp2)
        tmp2 = ""
print(blocks)

shuffle_list = []
for i in range(len(blocks)):
    shuffle_list.append(i)

shuffle_list = list(permutations(shuffle_list, len(blocks)))
candidate = []
for i in shuffle_list:
    tmp = ""
    for j in i:
        tmp += blocks[j]
    if tmp.startswith("FLAG{") and tmp.endswith("}"):
        candidate.append(tmp)

for i in candidate:
    # candidateの各要素のSHA256を求めて19B0E576B3457EDFD86BE9087B5880B6D6FAC8C40EBD3D1F57CA86130B230222と一致と一致する物だけを出力
    if (
        hashlib.sha256(i.encode()).hexdigest()
        == "19b0e576b3457edfd86be9087b5880b6d6fac8c40ebd3d1f57ca86130b230222"
    ):
        print(i)
