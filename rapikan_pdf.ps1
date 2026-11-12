# rapikan_pdf.ps1  --  menyalin dan mengganti nama PDF modul agar cocok dengan tautan README
# Cara pakai (Windows):
#   1. Buka folder yang berisi PDF "Modul 00 - ... .pdf" dst. (mis. C:\xampp\htdocs\MODUL_PROJECT)
#   2. Klik kanan di area kosong -> "Open in Terminal" (atau Shift + klik kanan -> Open PowerShell here)
#   3. Tempel seluruh isi berkas ini, tekan Enter
# Hasil: folder baru "pdf" berisi salinan dengan nama seperti 00-suite-erp-peta-hubungan.pdf
#        (berkas asli tidak diubah). Unggah isi folder "pdf" ke repositori GitHub.

$map = @{
    '00' = '00-suite-erp-peta-hubungan'
    '01' = '01-erp-inventaris'
    '02' = '02-erp-procura'
    '03' = '03-erp-mkp-keuangan'
    '04' = '04-erp-sdm-hris'
    '05' = '05-erp-paybridge-payroll'
    '06' = '06-cemwp'
    '07' = '07-kode-tebak-web'
    '08' = '08-bdw-blog'
    '09' = '09-perpustakaan-digital'
    '10' = '10-spk-keuangan'
    '11' = '11-tes-iq-eq'
    '12' = '12-toolkit-app'
    '13' = '13-visual-novel-harmoni-lima-hati'
    '14' = '14-kode-tebak-mobile'
    '15' = '15-fleetpro'
    '16' = '16-mepro'
    '17' = '17-profina'
    '18' = '18-tokolokal'
    '19' = '19-toolkit-app-public'
    '20' = '20-ficoim'
    '21' = '21-fraud-detection'
    '22' = '22-dospem'
    '23' = '23-stockfolio'
    '24' = '24-jasa-web'
}

$out = Join-Path (Get-Location) 'pdf'
New-Item -ItemType Directory -Force -Path $out | Out-Null

Get-ChildItem -Filter *.pdf -File | ForEach-Object {
    if ($_.Name -match '(?<!\d)(\d{2})(?!\d)') {
        $n = $Matches[1]
        if ($map.ContainsKey($n)) {
            $baru = $map[$n] + '.pdf'
            Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $out $baru) -Force
            Write-Host ("OK     {0}  ->  {1}" -f $_.Name, $baru)
            return
        }
    }
    Write-Host ("LEWATI {0}  (tidak ada nomor modul 00-24)" -f $_.Name)
}

$ada = Get-ChildItem -LiteralPath $out -Filter *.pdf | ForEach-Object { $_.Name.Substring(0,2) }
$belum = $map.Keys | Where-Object { $ada -notcontains $_ } | Sort-Object
if ($belum) { Write-Host ("`nNomor modul yang belum ada PDF-nya: " + ($belum -join ', ')) }
else { Write-Host "`nSemua 25 modul lengkap. Unggah isi folder 'pdf' ke GitHub." }
