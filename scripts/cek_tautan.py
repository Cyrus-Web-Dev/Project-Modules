#!/usr/bin/env python3
"""Memeriksa apakah semua PDF yang ditaut di README.md sudah ada di folder pdf/.
Jalankan dari root repositori:  python scripts/cek_tautan.py"""

import re
import sys
import pathlib
import urllib.parse

root = pathlib.Path(__file__).resolve().parent.parent
text = (root / "README.md").read_text(encoding="utf-8")

# Ambil semua tautan relatif pdf/...
raw_links = re.findall(r"\]\((pdf/[^)]+\.pdf)\)", text)

# Decode URL-encoding supaya bisa dicocokkan dengan nama file di disk
links = sorted(set(
    "pdf/" + urllib.parse.unquote(link[4:]) if link.startswith("pdf/") else link
    for link in raw_links
))

missing = [l for l in links if not (root / l).exists()]

print(f"{len(links)} PDF diperiksa, {len(missing)} belum ada.")
for m in missing:
    print("  - belum ada:", m)

sys.exit(1 if missing else 0)
