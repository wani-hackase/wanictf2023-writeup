---
title: shuffle_base64
level: 2
flag: FLAG{shuffle64}
writer: Gureisya
---

# shuffle_base64

## 問題文

シャッフルしてbase64エンコード確認！ヨシ！

FLAG shuffled, Base64-encoded. Wow!

```
FLAG format : FLAG{DUMMY_FLAG}
SHA256: 19B0E576B3457EDFD86BE9087B5880B6D6FAC8C40EBD3D1F57CA86130B230222
```


## 解法
FLAGに対する処理を見ると二文字ごとにランダムなアルファベットを追加し、最終的にFLAGの長さが3の倍数になるようにpadしている。そして、それらを3文字ずつのブロックに分けてランダムな並びにシャッフルしたものを結合してbase64エンコードしている。

というわけである程度逆に処理できそうなのでcipherをbase64デコードし、3の倍数番目の文字を取り除いていたものを2文字ずつブロックにしてitertools.permutationsなどで作ったシャッフルリストに当てはめてみると候補が得られる。

このままだと!(len(flag)//2)通りからFLAGを探さないといけないので 'FLAG{' から始まるものだけに絞るとかなり候補を減らせる。また、pad()でflagの長さが3の倍数でない時は余分なアルファベットが追加されるので '}' の後のアルファベットを取り除けば '}' で終わるものでさらに絞れる。

Looking at the processing for FLAG, it adds a random alphabet every two characters, pads it to make the length of FLAG a multiple of three. Then, it splits them into blocks of three characters and shuffles them randomly before concatenating and encoding them in base64.

Therefore, since it can be reversed to some extent, decoding the cipher in base64 and removing every third character to create blocks of two characters. You can use a shuffle list created using itertools.permutations and apply it to the blocks to get candidates.

As it is, you have to search for FLAG from !(len(flag)//2) possibilities, so narrowing it down to start with 'FLAG{' can significantly reduce the candidates. Also, if the length of the flag is not a multiple of three, pad() adds extra alphabets, so you can also use endswith('}') by removing the alphabet after '}'.
