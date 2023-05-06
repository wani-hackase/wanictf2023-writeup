---
title: 09. Copy & Paste
level: 5
flag: FLAG{d4n611n6_901n73r_3x1575}
writer: Caffeine
badge: true
---

# 09. Copy & Paste

## 問題文

メモの作成、閲覧、削除ができるheapの典型問題です。

メモをコピー&ペーストする機能を独自実装してみました。

`nc copy-paste-pwn.wanictf.org 9009`

______________________________________________________________________

It is a typical heap challenge where one can create, view and delete notes.
I have tried to implement a custom feature that enables copying and pasting of notes.

`nc copy-paste-pwn.wanictf.org 9009`

## 解法

[English ver.](#eng)

本問では、以下2つの脆弱性を利用してarbitrary address read (AAR)とarbitrary address write (AAW)の達成を目指す。

### Dangling pointer

本問ではメモはnote構造体の配列で管理される。
note構造体はメモの大きさとメモの内容へのポインタから構成される。

```c
typedef struct note {
  int size;
  char *ptr;
} note_t;
```

メモの内容は`malloc()`により動的に割り当てられたメモリに記録される。

ここで、`copy()`の実装をソースコードから確認する。

```c
void copy() {
  int idx;
  if ((idx = get_idx()) == -1)
    return;
  if (is_empty(idx))
    return;
  copied = list[idx];
  printf("Done!\n");
}
```

このように`copy()`はメモの内容をコピーしているわけではなく、実際にはnote構造体をグローバル変数`copied`に複製している。

続いて`delete()`の実装を確認する。

```c
void delete () {
  int idx;
  if ((idx = get_idx()) == -1)
    return;
  if (is_empty(idx))
    return;
  free(list[idx].ptr);
  list[idx].size = 0;
  list[idx].ptr = NULL;
  printf("Done!\n");
}
```

メモの内容を記録したメモリを`free()`により解放した後、当該note構造体のサイズを0に、ポインタをNULLに設定している。
これにより、単純なdouble freeやuse after free (UAF)は防がれる。

しかしながら、`delete()`の前に`copy()`を実行しておけばグローバル変数`copied`に解放されたメモリへのポインタが残る(いわゆるdangling pointer)。
`copied`に残ったポインタを参照して直接解放済みのチャンクを改ざんすることはできないが、以下の手順でチャンクの管理情報である`fd`を盗み見ることができる。

1. `create()`により適当なサイズのメモを作成する。
2. `create()`により十分大きなサイズかつ空のメモを作成する。
3. `copy()`により1で作成したメモを`copied`に複製する。
4. `delete()`により1で作成したメモを削除する。
5. `paste()`により2で作成したメモに`copied`を貼り付ける。
6. `show()`により`copied`が貼り付けられた2のメモを閲覧する。

解放するメモのサイズや各種binに繋がれるチャンクの個数を調整することで、heapやlibcのアドレスがリークできる。

### Heap overflow

メモのサイズと内容を調節することで`paste()`内でheap overflowが生じる。

`paste()`の大まかな動作は

1. 貼り付け先のメモを選択する。
2. 1で選択したメモと`copied`に格納されたメモを足したサイズのメモリを確保する。
3. 1で選択したメモと`copied`に格納されたメモの内容を結合したものを2で確保したメモリに記録する。
4. 1で選択したメモを削除する。代わりに2, 3の工程で作られた新たなメモを1で選択したメモとして登録する。

であり、実装は以下の通り。

```c
void paste() {
  int idx;
  note_t pasted;
  if ((idx = get_idx()) == -1)
    return;
  if (is_empty(idx))
    return;
  if (copied.ptr == NULL) {
    printf("Please copy a note before pasting!\n");
    return;
  }
  pasted.size = list[idx].size + copied.size;
  if (pasted.size < 0 || pasted.size > MAX_NOTE_SIZE) {
    printf("Invalid size!\nPaste failed!\n");
    return;
  }
  pasted.ptr = (char *)malloc(pasted.size);
  memset(pasted.ptr, 0, pasted.size);
  sprintf(pasted.ptr, "%s%s", list[idx].ptr, copied.ptr);
  free(list[idx].ptr);
  list[idx] = pasted;
  printf("Done!\n");
}
```
   
ここで`sprintf(pasted.ptr, "%s%s", list[idx].ptr, copied.ptr)`に着目する。
書式指定子`%s`は対応するポインタを文字列と解釈してNULLが現れるまで読み出す。
しかしながら、`create()`内ではメモの内容を標準入力から受け取った後、末尾にNULLを付加していない。

例えば、サイズ24のメモを1つだけ作成して内容をすべて'A'でパディングするとheap内部は以下のようになる。

```
0x561ef707e290  0x0000000000000000      0x0000000000000021      ........!.......
0x561ef707e2a0  0x4141414141414141      0x4141414141414141      AAAAAAAAAAAAAAAA
0x561ef707e2b0  0x4141414141414141      0x0000000000020d51      AAAAAAAAQ.......         <-- Top chunk
```

このメモに対して`paste()`により他のメモの貼り付けを行うことを考える。
貼り付け先のメモのサイズは24であるが、`sprintf(pasted.ptr, "%s%s", list[idx].ptr, copied.ptr)`では\x41\x41...\x41\x51\x0d\x02までの27バイト分が読み出される。
`copied`に設定するメモのサイズを16の倍数に設定した場合、`copied`の内容の末尾3バイトがoverflowする。

以上の操作によりチャンクの管理情報である`size`を書き換えることができる。
チャンクの`size`を書き換えることができれば、以下の手順で任意のアドレスをtcacheに繋げることができる。

1. Heap overflowを用いて割り当て済みのチャンク(victim chunk)の`size`を大きく書き換える。
```
before
                                        0x0000000000000031      AAAAAAAA1.......
0x55b8bc6902e0  0x000000055b8bc690      0xb36247d8d5a8cb51      ...[....Q....Gb.         <-- tcachebins[0x30][0/1]
0x55b8bc6902f0  0x0000000000000000      0x0000000000000000      ................
0x55b8bc690300  0x0000000000000000      0x0000000000000021      ........!.......
0x55b8bc690310  0x000a6d6974636976      0x0000000000000000      victim..........         <-- victim chunk
0x55b8bc690320  0x0000000000000000      0x0000000000000021      ........!.......
0x55b8bc690330  0x7070616c7265766f      0x00000000000a6465      overlapped......         <-- overlapped chunk
0x55b8bc690340  0x0000000000000000

after
                                        0x0000000000000031      AAAAAAAA1.......
0x55b8bc6902e0  0x4141414141414141      0x4141414141414141      AAAAAAAAAAAAAAAA
0x55b8bc6902f0  0x4141414141414141      0x4141414141414131      AAAAAAAA1AAAAAAA
0x55b8bc690300  0x4141414141414141      0x0000000000000041      AAAAAAAAA.......
0x55b8bc690310  0x000a6d6974636976      0x0000000000000000      victim..........         <-- victim chunk
0x55b8bc690320  0x0000000000000000      0x0000000000000021      ........!.......
0x55b8bc690330  0x7070616c7265766f      0x00000000000a6465      overlapped......         <-- overlapped chunk
0x55b8bc690340  0x0000000000000000
```

2. victim chunkとvictim chunkの次のチャンク(overlapped chunk)を解放する。
```
                                        0x0000000000000031      AAAAAAAA1.......
0x55b8bc6902e0  0x4141414141414141      0x4141414141414141      AAAAAAAAAAAAAAAA
0x55b8bc6902f0  0x4141414141414141      0x4141414141414131      AAAAAAAA1AAAAAAA
0x55b8bc690300  0x4141414141414141      0x0000000000000041      AAAAAAAAA.......
0x55b8bc690310  0x000000055b8bc690      0xb36247d8d5a8cb51      ...[....Q....Gb.         <-- victim chunk in tcachebins[0x40][0/1]
0x55b8bc690320  0x0000000000000000      0x0000000000000021      ........!.......
0x55b8bc690330  0x000055bde7e2c450      0xb36247d8d5a8cb51      P....U..Q....Gb.         <-- overlapped chunk in tcachebins[0x20][0/2]
0x55b8bc690340  0x0000000000000000
```
3. `create()`によりvictim chunkをtcacheから取り出す。メモの内容を書き込む際に、overlapped chunkの`fd`を改ざんして任意のアドレスをtcacheに繋げる。glibc2.35なのでsafe linkingが実装されている。突破するためには、dangling pointerを悪用してheapのアドレスを知っておく必要がある。

ここまで来たらAAWもAARも簡単。
書き込みたいアドレスをtcacheに繋いで`create()`により取り出せばAAWが達成できる。
AARは、まずサイズ0のメモとして読み出したいアドレスをtcacheから取り出した後に、適当なメモに対してこれを貼り付けることで達成できる。

AAWとAARが達成できれば、file structure oriented programming (FSOP)や`exit()`内で呼ばれるデストラクタの挙動を狙ってeipを奪うことができる(`_free_hook`や`_malloc_hook`などの便利なシンボルはglibc2.35にはありません)。

私の作成したエクスプロイト(solver以下にあります)では、libcにある変数`environ`からstackのアドレスをリークした後、AAWでstack上にROP chainを構築しています。

______________________________________________________________________

<a name="eng"></a>

In this challenge, we aim to achieve arbitrary address read (AAR) and arbitrary address write (AAW) by exploiting two vulnerabilities.

### Dangling pointer

In this challenge, notes are managed by an array of note structures.
Each note structure consists of the size of the note and a pointer to the content of the note.

```c
typedef struct note {
  int size;
  char *ptr;
} note_t;
```

The content of the note is recorded in dynamically allocated memory by `malloc()`.

Here, we will confirm the implementation of `copy()` from the source code.

```c
void copy() {
  int idx;
  if ((idx = get_idx()) == -1)
    return;
  if (is_empty(idx))
    return;
  copied = list[idx];
  printf("Done!\n");
}
```

Thus, `copy()` does not actually copy the contents of the note, but rather duplicates the note structure into the global variable `copied`.

Next, let's confirm the implementation of `delete()`.

```c
void delete () {
  int idx;
  if ((idx = get_idx()) == -1)
    return;
  if (is_empty(idx))
    return;
  free(list[idx].ptr);
  list[idx].size = 0;
  list[idx].ptr = NULL;
  printf("Done!\n");
}
```

After freeing the memory that stores the contents of the note, `delete()` sets the size of the corresponding note structure to 0 and the pointer to NULL.
This prevents simple double free and use after free (UAF) vulnerabilities.

However, if `copy()` is executed before `delete()`, a pointer to the released memory remains in the global variable `copied` (known as a dangling pointer).
Although it is not possible to directly tamper with the freed chunks by referencing the remaining pointer in `copied`, it is possible to steal the management information of the chunk, which is the `fd`, by following these steps.

1. Create a note of appropriate size using `create()`.
2. Create an empty note of sufficient size using `create()`.
3. Copy the note created in step 1 to `copied` using `copy()`.
4. Delete the note created in step 1 using `delete()`.
5. Paste `copied` into the note created in step 2 using `paste()`.
6. View the note created in step 2 with `show()`, which now contains the content of `copied`.

By adjusting the size of the memory to be freed and the number of chunks connected to each bin, it is possible to leak the address of the heap or libc.

### Heap overflow

By adjusting the size and content of the note, a heap overflow can occur within `paste()`.

`paste()` works roughly as follows:

1. Select the note to paste into.
2. Allocate memory for a new note that is the size of the selected note plus the size of the note stored in `copied`.
3. Combine the contents of the selected note and the note stored in `copied` and store them in the newly allocated memory.
4. Delete the selected note and register the new note created in steps 2 and 3.

The implementation is as follows:

```c
void paste() {
  int idx;
  note_t pasted;
  if ((idx = get_idx()) == -1)
    return;
  if (is_empty(idx))
    return;
  if (copied.ptr == NULL) {
    printf("Please copy a note before pasting!\n");
    return;
  }
  pasted.size = list[idx].size + copied.size;
  if (pasted.size < 0 || pasted.size > MAX_NOTE_SIZE) {
    printf("Invalid size!\nPaste failed!\n");
    return;
  }
  pasted.ptr = (char *)malloc(pasted.size);
  memset(pasted.ptr, 0, pasted.size);
  sprintf(pasted.ptr, "%s%s", list[idx].ptr, copied.ptr);
  free(list[idx].ptr);
  list[idx] = pasted;
  printf("Done!\n");
}
```
   
Let us focus on the `sprintf(pasted.ptr, "%s%s", list[idx].ptr, copied.ptr)`.
The format specifier `%s` reads characters from the corresponding pointer as a string until it encounters a NULL character.
However, `create()` does not append a NULL character to the end of the memory block after receiving input from standard input.

For instance, if we create a single note of size 24 and pad its content with 'A's, the internal structure of the heap would resemble the following.

```
0x561ef707e290  0x0000000000000000      0x0000000000000021      ........!.......
0x561ef707e2a0  0x4141414141414141      0x4141414141414141      AAAAAAAAAAAAAAAA
0x561ef707e2b0  0x4141414141414141      0x0000000000020d51      AAAAAAAAQ.......         <-- Top chunk
```

When considering pasting another note onto this note, it should be noted that the size of the target note is 24, but `sprintf(pasted.ptr, "%s%s", list[idx].ptr, copied.ptr)` reads up to 27 bytes including \x41\x41...\x41\x51\x0d\x02.
If the size of the note set to `copied` is a multiple of 16, the last 3 bytes of the content of `copied` will overflow.

By performing the above operations, we can overwrite the management information of a chunk, such as its `size`.
If we can overwrite `size` of a chunk, we can connect any address to the tcache by following these steps:

1. Use a heap overflow to overwrite `size` of an allocated chunk (victim chunk) with a larger value.
```
before
                                        0x0000000000000031      AAAAAAAA1.......
0x55b8bc6902e0  0x000000055b8bc690      0xb36247d8d5a8cb51      ...[....Q....Gb.         <-- tcachebins[0x30][0/1]
0x55b8bc6902f0  0x0000000000000000      0x0000000000000000      ................
0x55b8bc690300  0x0000000000000000      0x0000000000000021      ........!.......
0x55b8bc690310  0x000a6d6974636976      0x0000000000000000      victim..........         <-- victim chunk
0x55b8bc690320  0x0000000000000000      0x0000000000000021      ........!.......
0x55b8bc690330  0x7070616c7265766f      0x00000000000a6465      overlapped......         <-- overlapped chunk
0x55b8bc690340  0x0000000000000000

after
                                        0x0000000000000031      AAAAAAAA1.......
0x55b8bc6902e0  0x4141414141414141      0x4141414141414141      AAAAAAAAAAAAAAAA
0x55b8bc6902f0  0x4141414141414141      0x4141414141414131      AAAAAAAA1AAAAAAA
0x55b8bc690300  0x4141414141414141      0x0000000000000041      AAAAAAAAA.......
0x55b8bc690310  0x000a6d6974636976      0x0000000000000000      victim..........         <-- victim chunk
0x55b8bc690320  0x0000000000000000      0x0000000000000021      ........!.......
0x55b8bc690330  0x7070616c7265766f      0x00000000000a6465      overlapped......         <-- overlapped chunk
0x55b8bc690340  0x0000000000000000
```

2. Free the victim chunk and the next chunk (overlapped chunk).
```
                                        0x0000000000000031      AAAAAAAA1.......
0x55b8bc6902e0  0x4141414141414141      0x4141414141414141      AAAAAAAAAAAAAAAA
0x55b8bc6902f0  0x4141414141414141      0x4141414141414131      AAAAAAAA1AAAAAAA
0x55b8bc690300  0x4141414141414141      0x0000000000000041      AAAAAAAAA.......
0x55b8bc690310  0x000000055b8bc690      0xb36247d8d5a8cb51      ...[....Q....Gb.         <-- victim chunk in tcachebins[0x40][0/1]
0x55b8bc690320  0x0000000000000000      0x0000000000000021      ........!.......
0x55b8bc690330  0x000055bde7e2c450      0xb36247d8d5a8cb51      P....U..Q....Gb.         <-- overlapped chunk in tcachebins[0x20][0/2]
0x55b8bc690340  0x0000000000000000
```
3. Using `create()`, the victim chunk is retrieved from the tcache. When writing the contents of the note, the `fd` of the overlapped chunk is tampered with to link an arbitrary address to the tcache. Safe linking is implemented in glibc2.35, so it is necessary to know the address of the heap by exploiting the dangling pointer to break through.

At this point, both AAW and AAR are easy to accomplish.
To achieve AAW, we can simply link the address we want to write to the tcache and then retrieve it using `create()`.
For AAR, we can first retrieve the address we want to read as a note of size 0 from the tcache, and then paste it onto an arbitrary note.

Once AAW and AAR attacks are achieved, it is possible to get the eip by exploiting the File Structure Oriented Programming (FSOP) or the behavior of destructors called inside `exit()` function (useful symbols like `_free_hook` or `_malloc_hook` are not available in glibc2.35).

In my exploit (which is located in the solver directory), I first leak the stack address from the `environ` variable in libc and then use AAW to construct a ROP chain on the stack.
