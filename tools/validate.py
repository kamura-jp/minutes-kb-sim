#!/usr/bin/env python3
"""ナレッジ（YAML）の検証ツール（練習用）。

使い方:  python tools/validate.py [--kb-dir data/kb]
終了コード: 0=エラーなし / 1=エラーあり
"""
import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = ["id", "title", "body", "date", "source", "speaker", "confidentiality"]
ALLOWED_CONF = {"public", "internal", "confidential"}
ID_PATTERN = re.compile(r"^KB-\d{4}$")


def is_iso_date(value) -> bool:
    try:
        datetime.strptime(str(value), "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_entry(entry, raw_dir: Path):
    """1件分の問題点をメッセージのリストで返す。"""
    problems = []
    for key in REQUIRED:
        if key not in entry or entry[key] in (None, ""):
            problems.append(f"{key} が未入力です")
    if entry.get("id") and not ID_PATTERN.match(str(entry["id"])):
        problems.append(f"id の形式が不正です: {entry['id']}（例: KB-0001）")
    if entry.get("date") and not is_iso_date(entry["date"]):
        problems.append(f"date の形式が不正です: {entry['date']}（YYYY-MM-DD）")
    conf = entry.get("confidentiality")
    if conf and conf not in ALLOWED_CONF:
        problems.append(f"confidentiality が不正です: {conf}（{sorted(ALLOWED_CONF)}）")
    src = entry.get("source")
    if src and not (raw_dir / str(src)).exists():
        problems.append(f"source のファイルが data/raw に見つかりません: {src}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description="KB YAML validator")
    parser.add_argument("--kb-dir", default=str(ROOT / "data" / "kb"))
    args = parser.parse_args()
    kb_dir = Path(args.kb_dir)
    raw_dir = ROOT / "data" / "raw"

    errors = []
    seen_ids = {}
    total = 0
    for path in sorted(kb_dir.glob("*.yaml")):
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            errors.append(f"[ERROR] {path.name}: YAMLとして読めません: {exc}")
            continue
        for entry in (data or {}).get("entries", []):
            total += 1
            eid = entry.get("id", "(idなし)")
            if eid in seen_ids:
                errors.append(f"[ERROR] {path.name} {eid}: id が重複しています（{seen_ids[eid]} にもあります）")
            else:
                seen_ids[eid] = path.name
            for msg in validate_entry(entry, raw_dir):
                errors.append(f"[ERROR] {path.name} {eid}: {msg}")

    print(f"検査対象: {total} 件 / エラー: {len(errors)} 件")
    for line in errors:
        print(line)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
