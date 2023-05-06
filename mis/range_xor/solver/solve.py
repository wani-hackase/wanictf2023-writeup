path = "file/case(N=1000).txt"

A = []
f = open(path, "r")
A = f.read().split()
f.close()
A = [int(i) for i in A]
mod = 10**9 + 7


def f(a):
    return min(a, 1000 - a)


dp = [[0 for i in range(1024)] for j in range(1024)]
dp[0][A[0]] = 1
dp[0][f(A[0])] = 1

for i in range(len(A)):
    for j in range(1024):
        if dp[i][j] == 0:
            continue
        dp[i + 1][j ^ A[i]] += dp[i][j]
        dp[i + 1][j ^ A[i]] %= mod
        if j ^ A[i] != j ^ f(A[i]):
            dp[i + 1][j ^ f(A[i])] += dp[i][j]
            dp[i + 1][j ^ f(A[i])] %= mod

for i in range(1024):
    if dp[len(A)][i] != 0:
        print("FLAG{" + str(dp[len(A)][i]) + "}")
        break
