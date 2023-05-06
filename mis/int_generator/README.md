---
title: int_generator
level: 3
flag: FLAG{0_26476544_34359738368}
writer: Gureisya
---

# int_generator

## 問題文

0以上2**35以下の好きな整数を入れると16桁の整数になって返ってくる機械があります。
flag1, flag2, flag3はそれぞれ何でしょう？

There is a machine that takes any integer between 0 and 2**35 (inclusive) and returns a 16-digit integer.
What are flag1, flag2, and flag3?

FLAG format：FLAG{flag1_flag2_flag3}

## 解法
全探索でflagを見つけようとすると  2<sup>35</sup>+1 通り調べないといけないので厳しい

→ひとまず実験してみると奇数の割合が非常に多い

→outputが全て偶数であることから偶数になる条件を考える

int_generator()の返り値の偶奇はpad()の返り値の偶奇と一致するのでpad()を見る

pad()を見ると1つ目の引数が正→返り値が偶数、負→返り値が奇数
outputはいずれも偶数なので正の場合を考えたらよい

pad()の1つ目の引数が正となるのはどの場合か知るためにf(x)を見る

f(x)の返り値の正負は x<sup>2</sup> % r (ただし、r=2<sup>k</sup>) の偶奇によって変わり、
偶数のとき正、奇数のとき負となる

x<sup>2</sup> = 0 (mod r) となる場合を考えると x = r * i (i∈[0..2<sup>(k//2-1)</sup>], i∈Z)

2<sup>(k//2-1)</sup> = 2<sup>17</sup> であるので全探索が間に合う


To try to find the flag by exhaustive search, we have to examine 2<sup>35</sup>+1 patterns, which is tough.

→ For now, let's experiment and see that the proportion of odd numbers is very high.

→ Consider the condition for becoming even from the fact that all outputs are even.

The parity of the return value of int_generator() matches that of pad(), so check pad().

Looking at pad(), the return value is even if the first argument is positive, and odd if it is negative.
Since all outputs are even, consider only the positive case.

To know which case gives a positive value for the first argument of pad(), look at f(x).

The sign of the return value of f(x) depends on whether x<sup>2</sup> % r (where r = 2<sup>k</sup>) is even or odd, with positive for even and negative for odd.

Considering the case where x<sup>2</sup> = 0 (mod r), x = r * i (i ∈ [0..2<sup>(k//2-1)</sup>], i ∈ Z)

As 2<sup>(k//2-1)</sup> = 2<sup>17</sup>, exhaustive search is feasible.

