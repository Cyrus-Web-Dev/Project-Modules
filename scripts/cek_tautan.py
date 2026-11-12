#!/usr/bin/env python3
"""Memeriksa apakah semua PDF yang ditaut di README.md sudah ada di folder pdf/.
Jalankan dari root repositori:  python scripts/cek_tautan.py"""
import re, sys, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
text = (root / "README.md").read_text(encoding="utf-8")
links = sorted(set(re.findall(r"\]\((pdf/[^)]+\.pdf)\)", text)))
missing = [l for l in links if not (root / l).exists()]
print(f"{len(links)} PDF diperiksa, {len(missing)} belum ada.")
for m in missing:
    print("  - belum ada:", m)
sys.exit(1 if missing else 0)
