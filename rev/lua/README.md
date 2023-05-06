---
title: Lua
level: 2
flag: FLAG{1ua_0r_py4h0n_wh4t_d0_y0u_3ay_w4en_43ked_wh1ch_0ne_1s_be44er}
writer: hi120ki
---

# Lua

## 問題文

るあ〜

Lua~~~

---

配布ファイル`main.lua`のubuntuにおける実行方法

How to run `main.lua` on ubuntu

```
$ sudo apt update
$ sudo apt install lua5.1
$ lua main.lua
Input FLAG : FAKE{FAKE_FLAG}
Incorrect
```

## 解法

<https://github.com/kosuke14/ByteLuaObfuscator> を使って暗号化したLuaスクリプトを解読する問題です。

最後から1つ上の行を見ると、`CRYPTEDlIIlIIlI`という関数の出力結果を`CRYPTEDlIIlIlII`という関数に渡しています。

```lua
  return CRYPTEDlIIlIlII(CRYPTEDlIIlIIlI(CRYPTEDlIIllIll, CRYPTEDlIIlIIIl), getfenv(0))()
```

ここで`CRYPTEDlIIlIIlI`関数を確認すると

```lua
  local CRYPTEDlIIlIIlI = function(a, b)
    local c = CRYPTEDlIIlIlIl(CRYPTEDlIIlIllI(a))
    local d = c["\99\105\112\104\101\114"](c, CRYPTEDlIIlIllI(b))
    return CRYPTEDlIIlIllI(d)
  end
```

ここでローカル変数`d`の中身を表示できるよう`print(d)`を追加して実行し、中身を確認すると

```lua
  local CRYPTEDlIIlIIlI = function(a, b)
    local c = CRYPTEDlIIlIlIl(CRYPTEDlIIlIllI(a))
    local d = c["\99\105\112\104\101\114"](c, CRYPTEDlIIlIllI(b))
    print(d)
    return CRYPTEDlIIlIllI(d)
  end
```

```
G0x1YVEAAQQIBAgABQAAAAAAAABnZ195AAAAAAAAAAAAAAACBBQAAAAFAAAABkBAAEGAAAAcQAABBQAAAAbAQAALAEEAgUABAByAgAFBgAEAF0AAABbAAICFwAEAwQACAJxAAAEWgACAhcABAMFAAgCcQAABHgCAAAoAAAAEAwAAAAAAAABpbwAEBgAAAAAAAAB3cml0ZQAEDgAAAAAAAABJbnB1dCBGTEFHIDogAAQGAAAAAAAAAHN0ZGluAAQFAAAAAAAAAHJlYWQABAYAAAAAAAAAKmxpbmUABEMAAAAAAAAARkxBR3sxdWFfMHJfcHk0aDBuX3doNHRfZDBfeTB1XzNheV93NGVuXzQza2VkX3doMWNoXzBuZV8xc19iZTQ0ZXJ9AAQGAAAAAAAAAHByaW50AAQIAAAAAAAAAENvcnJlY3QABAoAAAAAAAAASW5jb3JyZWN0AAAAAAAUAAAAAQAAAAEAAAABAAAAAQAAAAIAAAACAAAAAgAAAAIAAAACAAAAAwAAAAQAAAAEAAAABQAAAAUAAAAFAAAABQAAAAcAAAAHAAAABwAAAAgAAAACAAAAAgAAAAAAAABhAAkAAAATAAAAAgAAAAAAAABiAAoAAAATAAAAAAAAAA==
Input FLAG :
```

このようにBase64エンコードされた文字列が出力されるので、これをデコードします。すると難読化されていたLuaプログラムに含まれる可読文字列が出力されます。

```
LuaQ gg_y io write Input FLAG : stdin read *line C FLAG{1ua_0r_py4h0n_wh4t_d0_y0u_3ay_w4en_43ked_wh1ch_0ne_1s_be44er} print Correct Incorrect
```

ここからフラグ`FLAG{1ua_0r_py4h0n_wh4t_d0_y0u_3ay_w4en_43ked_wh1ch_0ne_1s_be44er}`を得ることができます。

---

This is a challenge of deciphering a Lua script encrypted using the ByteLuaObfuscator tool available at <https://github.com/kosuke14/ByteLuaObfuscator>.

Looking at the line just above the last one, the output of the function called `CRYPTEDlIIlIIlI` is passed as an argument to another function named `CRYPTEDlIIlIlII`.

```lua
  return CRYPTEDlIIlIlII(CRYPTEDlIIlIIlI(CRYPTEDlIIllIll, CRYPTEDlIIlIIIl), getfenv(0))()
```

Now, let's check the function `CRYPTEDlIIlIIlI`.

```lua
  local CRYPTEDlIIlIIlI = function(a, b)
    local c = CRYPTEDlIIlIlIl(CRYPTEDlIIlIllI(a))
    local d = c["\99\105\112\104\101\114"](c, CRYPTEDlIIlIllI(b))
    return CRYPTEDlIIlIllI(d)
  end
```

Then, you can add a `print(d)` statement to display the contents of the local variable `d`
```lua
  local CRYPTEDlIIlIIlI = function(a, b)
    local c = CRYPTEDlIIlIlIl(CRYPTEDlIIlIllI(a))
    local d = c["\99\105\112\104\101\114"](c, CRYPTEDlIIlIllI(b))
    print(d)
    return CRYPTEDlIIlIllI(d)
  end
```

```
G0x1YVEAAQQIBAgABQAAAAAAAABnZ195AAAAAAAAAAAAAAACBBQAAAAFAAAABkBAAEGAAAAcQAABBQAAAAbAQAALAEEAgUABAByAgAFBgAEAF0AAABbAAICFwAEAwQACAJxAAAEWgACAhcABAMFAAgCcQAABHgCAAAoAAAAEAwAAAAAAAABpbwAEBgAAAAAAAAB3cml0ZQAEDgAAAAAAAABJbnB1dCBGTEFHIDogAAQGAAAAAAAAAHN0ZGluAAQFAAAAAAAAAHJlYWQABAYAAAAAAAAAKmxpbmUABEMAAAAAAAAARkxBR3sxdWFfMHJfcHk0aDBuX3doNHRfZDBfeTB1XzNheV93NGVuXzQza2VkX3doMWNoXzBuZV8xc19iZTQ0ZXJ9AAQGAAAAAAAAAHByaW50AAQIAAAAAAAAAENvcnJlY3QABAoAAAAAAAAASW5jb3JyZWN0AAAAAAAUAAAAAQAAAAEAAAABAAAAAQAAAAIAAAACAAAAAgAAAAIAAAACAAAAAwAAAAQAAAAEAAAABQAAAAUAAAAFAAAABQAAAAcAAAAHAAAABwAAAAgAAAACAAAAAgAAAAAAAABhAAkAAAATAAAAAgAAAAAAAABiAAoAAAATAAAAAAAAAA==
Input FLAG :
```

You will find that it outputs a string that is Base64 encoded. By decoding this string, readable characters within the obfuscated Lua program can be revealed.

```
LuaQ gg_y io write Input FLAG : stdin read *line C FLAG{1ua_0r_py4h0n_wh4t_d0_y0u_3ay_w4en_43ked_wh1ch_0ne_1s_be44er} print Correct Incorrect
```

Then, we got `FLAG{1ua_0r_py4h0n_wh4t_d0_y0u_3ay_w4en_43ked_wh1ch_0ne_1s_be44er}`!
