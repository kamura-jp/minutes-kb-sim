# 解答例（取り組んだあとに見る）

## T2：確認事項の例
- 10/12の議事録の「（発言者不明）: 保存期間は60日だったと思います」は、発言者が不明で、本人も確信がない。**登録しない**。
- 10/12の議事録の日付「令和8年10月12日」は2026-10-12に直せる。
- 「FAQの更新対象は24件」の発言は2回あり、同じ内容なので**1件にまとめる**。
- ログ保存期間は、10/5「90日で進める（法務確認が必要）」→ 10/12「法務で確認中」→ 10/19「180日で確定」と変わっている。**登録するのは10/19の180日**。90日は古い情報。
- 10/5の「予算の上限は未定」は、決まっていないという内容。金額は登録しない。

## T4：検証エラーと直し方
| 対象 | エラー | 直し方 |
|---|---|---|
| product.yaml KB-0003 | date が `2026/10/12` | `2026-10-12` にする |
| legal.yaml KB-0003 | id の重複 | 続き番号（KB-0007以降）に振り直す |
| legal.yaml KB-0004 | source が空 | `minutes_2026-10-19_legal.txt` を入れる |
| legal.yaml KB-0005 | confidentiality が `社外秘` | 許可された値に直す。10/19の議事録は「社内限定の資料」とあるので `internal` が妥当。迷う場合は確認事項に入れる |

## T6：文字コードと日付
- `feedback.csv` は Shift_JIS（cp932）。`--encoding utf-8` を指定すると「文字コードが合いません」と出る。
- 「10月22日」は年が書かれていない。**2026年と推測せず**、確認事項にする（ツールは「要確認」を出す）。
- 投稿者が空の行は「不明」になる。これも確認事項に入れてよい。

## T7：AI要約の照合結果
| # | AI要約 | 結果 | 根拠 |
|---|---|---|---|
| 1 | リリースは11月13日 | 誤り | 10/5の議事録では11月20日 |
| 2 | 予算の上限は500万円で確定 | 原資料にない | 10/5の議事録では「まだ決めていない」 |
| 3 | ログ保存期間は90日 | 古い情報 | 10/19の議事録で180日に確定 |
| 4 | FAQ更新対象は24件 | 一致 | 10/12の議事録 |
| 5 | 匿名化は11月10日までに実装予定 | 一致 | 10/19の議事録 |

## T8：SQLの例
```sql
SELECT id, title FROM entries;
SELECT * FROM entries WHERE confidentiality = 'internal';
SELECT speaker, COUNT(*) FROM entries GROUP BY speaker;
SELECT * FROM entries ORDER BY date DESC LIMIT 3;
SELECT id, COUNT(*) FROM entries GROUP BY id HAVING COUNT(*) > 1;
SELECT * FROM entries WHERE source = '' OR source IS NULL;
SELECT * FROM entries WHERE body LIKE '%保存%';
```
