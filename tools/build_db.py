#!/usr/bin/env python3
"""data/kb のYAMLを SQLite（kb.db）に取り込む（SQL練習用）。"""
import sqlite3
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
conn = sqlite3.connect(ROOT / "kb.db")
conn.execute("DROP TABLE IF EXISTS entries")
conn.execute(
    "CREATE TABLE entries (id TEXT, title TEXT, body TEXT, date TEXT,"
    " source TEXT, speaker TEXT, confidentiality TEXT, file TEXT)"
)
count = 0
for path in sorted((ROOT / "data" / "kb").glob("*.yaml")):
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    for e in data.get("entries", []):
        conn.execute(
            "INSERT INTO entries VALUES (?,?,?,?,?,?,?,?)",
            (e.get("id"), e.get("title"), e.get("body"), str(e.get("date") or ""),
             e.get("source"), e.get("speaker"), e.get("confidentiality"), path.name),
        )
        count += 1
conn.commit()
conn.close()
print(f"{count} 件を kb.db に取り込みました")
