# 議事録ナレッジ管理 擬似業務プロジェクト

社内向け生成AI「ミナト（架空）」が参照するナレッジを、正確に整理・更新する業務の練習用プロジェクトです。
求人にある次のスキルを、実際に手を動かして身につけることを目的にしています。

- 文書・議事録の整理と校正、原資料との照合（発言者・日付・出典）
- YAML/JSON/CSVの編集、文字コード・日付形式の扱い
- 既存Pythonツールの実行と、簡単な修正
- GitHub（ブランチ → 差分確認 → コミット → Pull Request）とGitHub Actionsの結果確認
- ログを使った一次切り分けと、エンジニアへの報告
- SQLによる基本的な抽出
- 生成AIの出力を原資料と照合する習慣

登場する会社・人物・数値はすべて架空です。

## あなたの役割
ナレッジ更新担当です。会議の議事録やフィードバックを読み、決まった形式（YAML）で登録します。
内容の最終判断は業務責任者、ツールの変更はエンジニアが行う想定で、あなたは「定型的なデータ作成・更新と一次切り分け」を担当します。

## フォルダ構成
```
data/raw/   原資料（議事録、フィードバックCSV、AI要約サンプル）
data/kb/    登録済みナレッジ（YAML）
tools/      validate.py（検証） / csv_to_yaml.py（CSV→YAML） / build_db.py（SQLite取り込み）
docs/       手順書、チェックリスト、エラー報告テンプレ、SQL練習、解答例
TASKS.md    課題一覧（T1〜T8）
.github/    GitHub Actions（PRのたびに validate.py を実行）
```

## セットアップ（Mac）
```bash
git clone <自分のリポジトリURL>
cd minutes-kb-sim
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python tools/validate.py
```
最初は検証エラーが出ます（課題T4で直します）。GitHub Actionsも最初は失敗（赤）になります。

## 進め方
1. このフォルダを自分のGitHubリポジトリにする（`git init` → GitHubで新規リポジトリ → push）。
2. `TASKS.md` の T1 から順に進める。必ずブランチを切り、Pull Requestで提出する。
3. 詰まったら、まず `docs/エラー報告テンプレ.md` の形で状況を書き出す（これも練習のうち）。
4. 終わったら、`docs/answers.md` の解答例と見比べる。

## ルール（本物の業務を想定）
- **推測で埋めない。** 曖昧なところは登録せず、確認事項として書き出す。
- **生成AIは使ってよい。** ただし出力は必ず原資料と照合し、変更内容と確認方法を自分の言葉で説明できること。
- **変更は必ずブランチ＋PR。** mainに直接コミットしない。
- **機密区分を必ず付ける。** `public` / `internal` / `confidential` のいずれか。
- 本番のデータや実在の個人情報は、このリポジトリに入れない。
