---
title: "whats_happening"
level: 1
flag: "FLAG{n0th1ng_much}"
writer: "Mikka"
---

# whats_happening

## 問題文

あなたはとあるファイルを入手しましたが、どうも壊れているようです……


You got a certain file, but it seems to be corrupted...

## 解法

バイナリエディタで中を見てFLAGで検索すると、FAKEと書かれたテキストファイルなどに混じってFLAG.pngがあることが分かる。

pngファイルのヘッダは臼NG (89 50 4E 47)で始まるのでこれを検索し、これに続くデータ部分を選択して保存する。

(別解)foremostコマンドを使用することで、pngを抽出できる。


By looking in a binary editor and searching for FLAG, you will see that there is FLAG.png and some FAKE files.

The header of PNG file starts with '89 50 4E 47', so search for this and select the data following it, then save it.

The png can also be extracted by using 'foremost' command.
