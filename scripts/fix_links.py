#!/usr/bin/env python3
"""
Memperbaiki tautan PDF di README.md agar sesuai dengan nama file asli
yang ada di folder pdf/ (tanpa merename file PDF).

Versi ini menggunakan URL-encoding agar tautan tetap valid
di dalam tabel Markdown GitHub.

Cara pakai (dari root repositori):
    python scripts/fix_links.py
"""

import re
import urllib.parse
from pathlib import Path

# Mapping: nama pendek (yang ada di README lama) → nama file asli
MAPPING = {
    "00-suite-erp-peta-hubungan.pdf": "Modul 00 — Suite ERP Peta Hubungan 5 Aplikasi.pdf",
    "01-erp-inventaris.pdf": "Modul 01 — ERP Inventaris.pdf",
    "02-erp-procura.pdf": "Modul 02 — ERP PROCURA (Pengadaan).pdf",
    "03-erp-mkp-keuangan.pdf": "Modul 03 — ERP MKP (Keuangan).pdf",
    "04-erp-sdm-hris.pdf": "Modul 04 — ERP SDM HRIS.pdf",
    "05-erp-paybridge-payroll.pdf": "Modul 05 — ERP PAYBRIDGE (Payroll).pdf",
    "06-cemwp.pdf": "Modul 06 — CEMWP (Connected Commerce).pdf",
    "07-kode-tebak-web.pdf": "Modul 07 — Kode Tebak v2.5.pdf",
    "08-bdw-blog.pdf": "Modul 08 — BDW (Blog Developer).pdf",
    "09-perpustakaan-digital.pdf": "Modul 09 — Perpustakaan Digital.pdf",
    "10-spk-keuangan.pdf": "Modul 10 — SPK (Pengelolaan Keuangan).pdf",
    "11-tes-iq-eq.pdf": "Modul 11 — Tes IQ & EQ v2.pdf",
    "12-toolkit-app.pdf": "Modul 12 — Toolkit App.pdf",
    "13-visual-novel-harmoni-lima-hati.pdf": "Modul 13 — Visual Novel Harmoni Lima Hati.pdf",
    "14-kode-tebak-mobile.pdf": "Modul 14 — Kode Tebak Mobile.pdf",
    "15-fleetpro.pdf": "Modul 15 — FLEETPRO (Logistik & Armada).pdf",
    "16-mepro.pdf": "Modul 16 — MEPRO (Manufacturing Execution System).pdf",
    "17-profina.pdf": "Modul 17 — PROFINA (SSO Suite).pdf",
    "18-tokolokal.pdf": "Modul 18 — TokoLokal (Kasir UMKM).pdf",
    "19-toolkit-app-public.pdf": "Modul 19 — Toolkit App (Public Edition).pdf",
    "20-ficoim.pdf": "Modul 20 — FICOIM (Finance Control & Inventory Management).pdf",
    "21-fraud-detection.pdf": "Modul 21 — Sistem Deteksi Financial Fraud (Skripsi Statistika).pdf",
    "22-dospem.pdf": "Modul 22 — DOSPEM (Dosen Pembimbing Digital).pdf",
    "23-stockfolio.pdf": "Modul 23 — StockFolio (Stock Portfolio Tracker & Analytics).pdf",
    "24-jasa-web.pdf": "Modul 24 — JASA-WEB (Web Jasa Pembuatan Project).pdf",
}

REPO = "Cyrus-Web-Dev/Project-Modules"
RAW_BASE = f"https://github.com/{REPO}/raw/main/pdf/"


def main():
    root = Path(__file__).resolve().parent.parent
    readme_path = root / "README.md"

    if not readme_path.exists():
        print("Error: README.md tidak ditemukan.")
        return 1

    content = readme_path.read_text(encoding="utf-8")
    original = content
    replaced = 0

    for short, actual in MAPPING.items():
        encoded = urllib.parse.quote(actual)

        # 1. Ganti tautan relatif (kolom Baca) — HARUS di-encode
        #    Menangani baik yang masih pendek maupun yang sudah diganti sebelumnya (belum encode)
        for old_rel in [
            f"(pdf/{short})",
            f"(pdf/{actual})",          # versi sebelumnya (belum encode)
        ]:
            new_rel = f"(pdf/{encoded})"
            if old_rel in content:
                content = content.replace(old_rel, new_rel)
                replaced += 1

        # 2. Ganti tautan full raw (kolom Unduh)
        new_raw = f"{RAW_BASE}{encoded}"

        for old_raw in [
            f"https://github.com/Cyrus-Web-Dev/project-modules/raw/main/pdf/{short}",
            f"https://github.com/Cyrus-Web-Dev/Project-Modules/raw/main/pdf/{short}",
            f"https://raw.githubusercontent.com/Cyrus-Web-Dev/project-modules/main/pdf/{short}",
            f"https://raw.githubusercontent.com/Cyrus-Web-Dev/Project-Modules/main/pdf/{short}",
            # versi yang sudah diganti sebelumnya tapi belum benar
            f"https://github.com/Cyrus-Web-Dev/Project-Modules/raw/main/pdf/{actual}",
            f"https://github.com/Cyrus-Web-Dev/project-modules/raw/main/pdf/{actual}",
        ]:
            if old_raw in content:
                content = content.replace(old_raw, new_raw)
                replaced += 1

    # Perbaiki teks tautan yang mungkin rusak (ada spasi aneh setelah [ )
    content = re.sub(r'\[\s*Baca\s*\]', '[📖 Baca]', content)
    content = re.sub(r'\[\s*📖\s*Baca\s*\]', '[📖 Baca]', content)

    if content == original:
        print("Tidak ada tautan yang perlu diperbaiki (sudah sesuai).")
        return 0

    # Backup
    backup_path = root / "README.md.bak"
    backup_path.write_text(original, encoding="utf-8")
    print(f"Backup dibuat: {backup_path.name}")

    readme_path.write_text(content, encoding="utf-8")
    print(f"README.md berhasil diperbarui ({replaced} penggantian).")
    print()
    print("Sekarang lakukan:")
    print("  1. python scripts/cek_tautan.py")
    print("  2. git add README.md")
    print('  3. git commit -m "Fix PDF links (URL-encoded for GitHub tables)"')
    print("  4. git push")
    print()
    print("Setelah di-push, refresh halaman GitHub untuk melihat hasilnya.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
