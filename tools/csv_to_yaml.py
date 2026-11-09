#!/usr/bin/env python3
"""フィードバックCSVをYAMLの下書きに変換するツール（練習用）。

使い方:
  python tools/csv_to_yaml.py --input data/raw/feedback.csv --output out/feedback_draft.yaml
オプション:
  --encoding  CSVの文字コード（既定: cp932）
  --start-id  最初のID番号（既定: 100 → KB-0100）
出力はそのまま data/kb に置かず、内容を確認してから移すこと。
"""
import argparse
import csv
import re
import sys
from pathlib import Path

import yaml


def normalize_date(text: str) -> str:
    """YYYY/MM/DD または YYYY-MM-DD を YYYY-MM-DD にそろえる。年が不明なら「要確認」。"""
    m = re.fullmatch(r"(\d{4})[/-](\d{1,2})[/-](\d{1,2})", text.strip())
    if not m:
        return "要確認"
    year, month, day = map(int, m.groups())
    return f"{year:04d}-{month:02d}-{day:02d}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--encoding", default="cp932")
    parser.add_argument("--start-id", type=int, default=100)
    args = parser.parse_args()

    src = Path(args.input)
    try:
        text = src.read_text(encoding=args.encoding)
    except UnicodeDecodeError as exc:
        print(f"文字コードが合いません（{args.encoding}）: {exc}", file=sys.stderr)
        return 1

    entries = []
    for i, row in enumerate(csv.DictReader(text.splitlines())):
        entries.append({
            "id": f"KB-{args.start_id + i:04d}",
            "title": f"{row['関連FAQ']} へのフィードバック",
            "body": row["内容"].strip(),
            "date": normalize_date(row["受付日"]),
            "source": src.name,
            "speaker": row["投稿者"].strip() or "不明",
            "confidentiality": "internal",
        })

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        yaml.safe_dump({"entries": entries}, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    print(f"{len(entries)} 件を {out} に書き出しました")
    return 0


if __name__ == "__main__":
    sys.exit(main())
