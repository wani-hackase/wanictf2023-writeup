---
title: EZDORSA_Lv3
level: 3          
flag: FLAG{fact0r1z4t10n_c4n_b3_d0n3_3as1ly}
writer: Gureisya      
---

# EZDORSA_Lv3

## 問題文

すうがくのちからってすげー！

The power of mathematics is staggering!

## 解法
nは25bitの異なる素数同士の積であるので素因数を全探索することができる。よってφ関数を求めることで復号できる。

Since n is the product of several distinct prime numbers each with 25 bits, we can exhaustively search for its prime factors.
Therefore, we can decrypt it by calculating　the value of the Euler's totient function (φ function).
