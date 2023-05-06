---
title: EZDORSA_Lv2  
level: 2          
flag: FLAG{l0w_3xp0n3nt_4ttAck}
writer: Gureisya      
---

# EZDORSA_Lv2

## 問題文

おや、eのようすが...?

What? e is too small?

## 解法
eが小さいことからe乗根を取ればmが得られる。cには5^100が掛かっているので割ってから求めたらよい（5^100はnよりも小さいので気にしなくてよい）。

In this cipher, you can obtain m by taking the e-th root of c, which is known because e is small. Since c is multiplied by 5^100, you should divide it before taking the root.
