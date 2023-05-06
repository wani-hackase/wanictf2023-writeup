p = 3
q = 5
n = p * q
e = 65535
d = 3
c = 10

# 秘密鍵を全探索した場合
for i in range(n):
    if pow(i, e, n) == c:
        print("FLAG{THE_ANSWER_IS_" + str(i) + "}")

# 秘密鍵が分かっていた場合
print("FLAG{THE_ANSWER_IS_" + str(pow(c, d, n)) + "}")
