---
title: "lowkey_messedup"
level: 2
flag: "FLAG{Big_br0ther_is_watching_y0ur_keyb0ard}"
writer: "Mikka"
---

# lowkey_messedup

## 問題文

誰も見てないよね……？


No one is watching me, right...?

## 解法

USBのパケットで、データが少なく頻度も少ないので、キーボードの通信であると予想できる。

pcapファイルでhostに送信されているパケットのデータ部分を見ると、2桁の16進数か、それに0x020000が加算されたものが送信されていることが分かる。

5,6文字目にある2桁の16進数は、そのままHIDキーコードと対応している。(aAが0x04, bBが0x05...)

一般的にUSBキーボードのパケットのデータ部分では、最初の文字が0x02ならLeft Shiftが同時押しされており、0x00なら何も押されていないことになる。(つまり大文字小文字の判定ができる。)

またbackspace(0x2A)が混じっているため、文字を削除する必要がある。

The pcap file is USB packets with small and infrequent data, so we can expect it to be a keyboard connection.

Looking at the data of the packet sent to the host, we can see that it contains a two-digit hex number or a number with 0x020000 added to it.

The two-digit hex number in the fifth and sixth characters corresponds directly to the HID key code. (like 0x04 for aA, 0x05 for bB)

In the data of the packet, if the first character is 0x02, it means Left Shift is being pressed. if 0x00, Shift is not being pressed. So you can check if a letter is upper or lower case.

Also, backspace (0x2A) is mixed in, so some characters need to be deleted.