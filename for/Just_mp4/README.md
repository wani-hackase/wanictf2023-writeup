---
title: "Just_mp4"
level: 1
flag: "FLAG{H4v1n_fun_1nn1t}"
writer: "Mikka"
---

## 問題文

✨✨✨ Enjoy wani CTF ! ✨✨✨

## 解法

画像のプロパティにflag_base64:～と書いてあるので、これを見つけてbase64デコードする。

もしくは、`exiftool chall.mp4`をする。

There is 'flag_base64:-' in property of the image, so find this and base64 decode it.

You can also do `exiftool chall.mp4`.