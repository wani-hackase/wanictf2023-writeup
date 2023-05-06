---
title: DSA?
level: 4
flag: "FLAG{trivial&baby_dsa_puzzle}"
writer: Badlylucky
badge: true
---

# DSA?

## 問題文

📨

```
nc dsa-cry.wanictf.org 50010
```

## 解法

The problem gives a general DSA algorithm. But this implementation makes a random integer $k$ from the message (=FLAG). Therefore, the sign in this problem algorithm is the following equation.

$$
\begin{eqnarray}
sign &=& FLAG * (\mathrm{SHA256}(FLAG) + x*g^{FLAG}) \pmod{q} \\
 &=& FLAG * \mathrm{SHA256}(FLAG) + FLAG * x * g^{FLAG} \pmod{q}
\end{eqnarray}
$$

$FLAG$, $q$ and $g$ are constant and we know them, but $x$ is secret and we don't know it. So this signature is secure!

No. This signature has a vulnerability in the message. That is, it  sends exactly the same message every time. This vulnerability causes the signatures to partially match in the signatures obtained by repeating to sign with different $x$s. In the above formula $FLAG\*\mathrm{SHA256}(FLAG)$ is always the same value, so we subtract one signature from another and we can separate $FLAG\*z$ ($z$ is a new unknown value) from two signatures.

In many cases, $z$ is much larger than $FLAG$, but we can treat $z$ as a random value. So the GCD of all $z$s becomes 1 by collecting many $z$s. On the other hand, $FLAG$ is constant. So we can recover $FLAG$ by collecting many $(FLAG\*z)$​s and calculating the GCD of all $(FLAG\*z)$​s.
