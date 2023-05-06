---
title: IndexedDB
level: 1
flag: FLAG{y0u_c4n_u3e_db_1n_br0wser}
writer: hi120ki
badge: true
---

# IndexedDB

## 問題文

このページのどこかにフラグが隠されているようです。ブラウザの開発者ツールを使って探してみましょう。

It appears that the flag has been hidden somewhere on this page. Let's use the browser's developer tools to find it.

<https://indexeddb-web.wanictf.org>

## 解法

問題ページにアクセスすると`Flag is already hidden in this page.`と表示されます。

開発者ツールを開き、Applicationの項目を見ていくとIndexedDBの中に`testDB`という項目があります。

`testDB`を開くと`testObjectStore`があり、その中に`FALG`という項目があり、フラグを取得できます。

---

Upon accessing the problem page, the message `Flag is already hidden in this page.` is displayed.

By opening the developer tools and navigating to the Application section, an item called `testDB` can be found within the IndexedDB.

Opening `testDB` reveals the existence of `testObjectStore`, wherein lies the `FALG` item and the flag can be obtained.
