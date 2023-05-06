---
title: range_xor
level: 2
flag: FLAG{461905191}
writer: Gureisya
---

# range_xor

## 問題文

整数列Aの任意の要素a_i(0<=a_i<=1000,i=1,2...N)に対して操作fを次のように定める

For any element a_i (0 <= a_i <= 1000, i = 1, 2, ..., N) of the integer sequence A, the operation f is defined as follows:

```
f(a_i)=min(a_i, 1000-a_i)
```

操作fを好きな回数行った後の整数列B={b_1,b_2...b_N}に対して

For the integer sequence B = {b_1, b_2, ..., b_N} obtained after applying operation f any number of times,

```
X = b_1 xor b_2 xor ... xor b_N
```

とするとき、Xを最小にするような整数列Bの種類数を
10^9+7で割った余りをFLAGとする。

Find the number of distinct integer sequences B that minimize X, and take the result modulo 10^9 + 7 as the FLAG.


__Test Case__

N=3, A={10, 20, 55}の時、
X=41が最小値となり、そのようなXを作るBは
B={10, 20, 55}の1種類である。
よってFLAG{1}

When N=3 and A={10, 20, 55}, X=41 is the smallest value and there is only one type of B that produces such X, which is B={10, 20, 55}.
Therefore, the answer is FLAG{1}.

N=10, A={532, 746, 606, 601, 293, 825, 912, 826, 789, 190}の時、
X=32が最小値となり、そのようなXを作るBは2種類である。
よってFLAG{2}

When N=10 and A={532, 746, 606, 601, 293, 825, 912, 826, 789, 190}, X=32 is the smallest value and there are two types of B that produce such X.
Therefore, the answer is FLAG{2}.

## 解法
それぞれのa_iに対してfを適用する場合としない場合を試していくと計算量はO(2^(len(A)))となる。
len(A)=1000であるためナイーブな方法は不可能である。

If we try applying f to each a_i or not, the computational complexity becomes O(2^(len(A))). Since len(A)=1000, a naive method is impossible.

というわけでDPを使ってみる。len(A[i]) < 1024 かつ 0 <= a_i, f(a_i) <= 1000 であることから dp[1024][1024] を確保して

So, let's try to use DP. Since len(A[i]) < 1024 and 0 <= a_i, f(a_i) <= 1000, we can allocate dp[1024][1024].

```
dp[i+1][j^A[i]] += dp[i][j]
dp[i+1][j^f(A[i])] += dp[i][j]
dp[i+1][j^A[i]] %= (10**9+7)
dp[i+1][j^f(A[i])] %= (10**9+7)
```
と遷移していけばよい。
ただし、A[i] = f(A[i])の時に注意。

We can transition as described above. However, be careful when A[i] = f(A[i]).
