# SQL練習

準備: `python tools/build_db.py` を実行すると `kb.db` ができます。
開き方: `sqlite3 kb.db`（終了は `.quit`）。見やすくするには `.headers on` と `.mode column`。

テーブル: `entries(id, title, body, date, source, speaker, confidentiality, file)`

## 問い
1. 全件の `id` と `title` を表示する。
2. `confidentiality` が `internal` のものだけを表示する。
3. 発言者（`speaker`）ごとの件数を数える。
4. `date` が新しい順に並べ、上位3件を表示する。
5. 同じ `id` が複数ある行を探す（`GROUP BY` と `HAVING`）。
6. `source` が空の行を探す。
7. `body` に「保存」を含む行を探す（`LIKE`）。

## ヒント
- 3: `GROUP BY speaker` と `COUNT(*)`
- 5: `GROUP BY id HAVING COUNT(*) > 1`
- 6: `WHERE source = '' OR source IS NULL`
