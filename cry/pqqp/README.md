---
title: pqqp
level: 3
flag: FLAG{p_q_p_q_521d0bd0c28300f}
writer: Laika
---

# pqqp

## 問題文

✨

## 解法

$s \\equiv p^q + q^p \\mod n$ に注目する。
整数 $k$ を用いて $s = p^q + q^p + kn$ と表せるので、 $s \\mod p, s \\mod q$ をそれぞれ計算すると\
フェルマーの小定理より

$$
\\begin{aligned}
s \\equiv q^p \\equiv q \\mod p\\
s \\equiv p^q \\equiv p \\mod q
\\end{aligned}
$$

となる。

以上の結果とChinese Remainder Theoremより、 $s = p+q$ であることがわかる。
二次方程式 $x^2 -sx + n = 0$ の解は $x = p, q$ となるので、これらの値からRSA暗号を復号できた。

______________________________________________________________________

Let us express $s$ as $s = p^q + q^p + kn$ where $k$ is an integer.
By calculating $s \\mod p$ and $s \\mod q$, we can apply Fermat's little theorem to obtain

$$
\\begin{aligned}
s \\equiv q^p \\equiv q \\mod p\\
s \\equiv p^q \\equiv p \\mod q
\\end{aligned}
$$

Using the Chinese remainder theorem together with the above results, we can conclude that $s = p+q$. Therefore, the solutions of the quadratic equation $x^2 -sx + n = 0$ are $x = p, q$. We can use these values to decrypt the ciphertext.
