---
title: "fusion"
level: 3
flag: "FLAG{sequ4ntia1_prim4_fact0rizati0n}"
writer: "Badlylucky"
---
# fusion
## 問題文
🧬

## 解法
The output.txt gives the RSA public keys and the 1024-bit integer $r$, where $r$ is made up of $p$'s odd-numbered bits and $q$'s even-numbered bits. We apply the appropriate mask to $r$ and retrieve $p$'s odd-numbered bits and $q$'s even-numbered bits.

Using these two parts and $N$, we can recover $p$ and $q$. If we know the lower $k$ bits of $p$ and $q$, the lower $k$ bit of $pq$ is equal to the lower $k$ bit of $N$. In this situation, we know the lower $k$ bits of $p$ and the lower $k-1$ bits of $q$. So we can do a bruteforce attack on the $k$th bit of $q$ and apply the bit if the lower $k$ bit of $pq$ is equal to the lower $k$ bit of $N$. This is because the $k$th bit of $q$ is just two patterns, $0$ or $1$.

In the solver, be careful of swapping alternatively $p$ and $q$ of this writeup in one iteration.
