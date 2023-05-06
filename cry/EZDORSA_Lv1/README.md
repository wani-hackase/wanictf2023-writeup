---
title: EZDORSA_Lv1    
level: 1          
flag: FLAG{THE_ANSWER_IS_10}
writer: Gureisya      
---

# EZDORSA_Lv1

## 問題文

はじめまして！RSA暗号の世界へようこそ！

この世界ではRSA暗号と呼ばれる暗号がいたるところで使われておる！

それでは手始めに簡単な計算をしてみよう！

- p = 3
- q = 5
- n = p*q
- e = 65535
- c ≡ m^e (mod n) ≡ 10 (mod n)

以上を満たす最小のmは何でしょう？
FLAG{THE_ANSWER_IS_?}の？にmの値を入れてください。


Hello there! Welcome to the world of RSA! 

In this world, there exists a crypto called RSA.

Let's start with a simple calculation!

- p = 3
- q = 5
- n = p*q
- e = 65535
- c ≡ m^e (mod n) ≡ 10 (mod n)

What is the smallest value of m that satisfies the above conditions?
Please substitute the value of m into the "?" in FLAG{THE_ANSWER_IS_?}.

## 解法
RSA暗号の復号に関する問題です。mを全探索することで解くことが出来ます。

This is a problem related to the decryption of RSA cipher. It can be solved by exhaustively searching the m.
