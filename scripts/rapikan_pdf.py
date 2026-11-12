#!/usr/bin/env python3
"""Menyamakan nama berkas di folder pdf/ dengan nama yang dipakai README.

Cara kerja: nomor modul (dua digit, mis. 00, 07, 24) di nama berkas dicocokkan dengan
daftar di bawah. Contoh:  "Modul 05 - ERP PAYBRIDGE (Payroll).pdf"  ->  05-erp-paybridge-payroll.pdf

Pemakaian (dari root repositori):
    python scripts/rapikan_pdf.py            # hanya menampilkan rencana (aman)
    python scripts/rapikan_pdf.py --apply    # benar-benar mengganti nama
"""
import re, sys, pathlib

NAMA = {
    "00": "00-suite-erp-peta-hubungan",
    "01": "01-erp-inventaris",
    "02": "02-erp-procura",
    "03": "03-erp-mkp-keuangan",
    "04": "04-erp-sdm-hris",
    "05": "05-erp-paybridge-payroll",
    "06": "06-cemwp",
    "07": "07-kode-tebak-web",
    "08": "08-bdw-blog",
    "09": "09-perpustakaan-digital",
    "10": "10-spk-keuangan",
    "11": "11-tes-iq-eq",
    "12": "12-toolkit-app",
    "13": "13-visual-novel-harmoni-lima-hati",
    "14": "14-kode-tebak-mobile",
    "15": "15-fleetpro",
    "16": "16-mepro",
    "17": "17-profina",
    "18": "18-tokolokal",
    "19": "19-toolkit-app-public",
    "20": "20-ficoim",
    "21": "21-fraud-detection",
    "22": "22-dospem",
    "23": "23-stockfolio",
    "24": "24-jasa-web",
}

root = pathlib.Path(__file__).resolve().parent.parent
pdf_dir = root / "pdf"
apply = "--apply" in sys.argv

berkas = sorted(p for p in pdf_dir.glob("*") if p.suffix.lower() == ".pdf")
if not berkas:
    sys.exit("Folder pdf/ belum berisi berkas .pdf")

rencana, dilewati, terpakai = [], [], {}
for f in berkas:
    cocok = re.search(r"(?<!\d)(\d{2})(?!\d)", f.stem)
    if not cocok or cocok.group(1) not in NAMA:
        dilewati.append((f.name, "tidak ada nomor modul 00-24 pada nama"))
        continue
    no = cocok.group(1)
    if no in terpakai:
        dilewati.append((f.name, f"nomor {no} sudah dipakai oleh {terpakai[no]}"))
        continue
    terpakai[no] = f.name
    baru = NAMA[no] + ".pdf"
    rencana.append((f, pdf_dir / baru))

for lama, baru in rencana:
    if lama.name == baru.name:
        print(f"  sudah benar : {lama.name}")
    else:
        print(f"  {lama.name}  ->  {baru.name}")
        if apply:
            if baru.exists():
                print("     ! dilewati, sudah ada berkas bernama itu")
            else:
                lama.rename(baru)
for nama, alasan in dilewati:
    print(f"  ! dilewati  : {nama} ({alasan})")

belum = [n for n in sorted(NAMA) if n not in terpakai]
if belum:
    print("\nNomor modul yang belum punya PDF:", ", ".join(belum))
print("\n" + ("Selesai mengganti nama." if apply else "Ini hanya rencana. Jalankan lagi dengan --apply untuk mengganti nama."))
