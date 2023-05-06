---
title: "beg_for_a_peg"
level: 3
flag: "FLAG{Hug_a_pug_less_than_three}"
writer: "Mikka"
---

# beg_for_a_peg

## 問題文

ある通信で受け渡されている画像ファイルをのぞき見てみましょう……


Just take a look at the image files being passed in a certain traffic...

## 解法

wiresharkでpcapファイルを開き、「flag.jpg」というファイルが他のjpgファイルとともに送受信されていることを確認する。

右クリック→追跡→TCPストリームとするとこの画像に関するパケットのみを表示することができるので、raw(無加工)形式にしてjpgファイルとして保存する。

開けない場合は、jpgのヘッダであるffd8～を探してそれ以前のデータをバイナリエディタで消去すれば良い。


Open the pcap file in wireshark and check that the file 'flag.jpg' is being sent and received.

Note that there are also other files.

You can 'Follow TCP Stream' to view only the packets related to a certain file, and save it as a jpg file in 'raw format'.

If you cannot open it, look for 'ff d8 ...' which is the header of jpg in binary editor, and erase the data before that.
