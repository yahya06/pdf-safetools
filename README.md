# PDF SafeTools

**PDF Utility & Security Tool for Windows**

> Merge • Split • Compress • Organize • Scan • Sanitize

PDF SafeTools adalah aplikasi desktop Windows untuk pengolahan, pemeriksaan, dan sanitasi dokumen PDF secara lokal. Semua pemrosesan berjalan di komputer pengguna — tanpa server, tanpa cloud, tanpa unggah dokumen.

---

## Fitur

### PDF Tools

- Merge PDF
- Split PDF
- Rotate PDF
- Delete Page
- Reorder Page
- Extract Page
- Compress PDF
- PDF → Image
- Image → PDF
- PDF Information

### PDF Security

- Scan PDF (static analysis)
- Sanitize PDF
- JKN Safe Mode preset
- Security report
- Re-scan setelah sanitasi

---

## Prinsip

```
LOCAL FIRST
PRIVACY FIRST
SECURITY FIRST
NO CLOUD
```

- Semua pemrosesan PDF berjalan lokal di komputer pengguna.
- Tidak ada unggahan PDF ke cloud atau API pihak ketiga.
- Tidak ada pengiriman dokumen ke AI atau online malware scanner.
- Operasi PDF utama berjalan tanpa koneksi internet.
- File original tidak pernah ditimpa; output menggunakan suffix `_clean`, `_compressed`, atau `merged.pdf`.

---

## Persyaratan Sistem

```
Windows 10 / 11 (x64)
```

Untuk pengguna akhir (versi installer/exe): tidak perlu menginstall Python, pip, atau Git.

Untuk pengembangan:

```
Windows 10/11
Python 3.12+
Git
Ghostscript (saat fitur compress diaktifkan)
```

---

## Instalasi — Pengguna Akhir

Installer Windows tersedia di halaman [Releases](https://github.com/yahya06/pdf-safetools/releases). Pilih release terbaru, unduh `PDFSafeTools-Setup.exe`, lalu jalankan installer. Python dan Git tidak diperlukan pada mesin pengguna. Ghostscript harus dipasang terpisah jika fitur compression digunakan.

---

## Instalasi — Pengembangan

### 1. Clone repository

```powershell
git clone https://github.com/yahya06/pdf-safetools.git
cd pdf-safetools
```

### 2. Buat virtual environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependency

```powershell
pip install -r requirements.txt
```

Untuk development (termasuk ruff, mypy, pytest):

```powershell
pip install -r requirements-dev.txt
```

### 4. Jalankan aplikasi

```powershell
python -m app.main
```

### 5. Update source code

Jika repository sudah pernah di-clone:

```powershell
git checkout main
git pull origin main
```

Jika ingin mengambil versi terbaru dari awal:

```powershell
git clone https://github.com/yahya06/pdf-safetools.git
cd pdf-safetools
```

Setelah update dependency atau berpindah branch, jalankan kembali:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Mendapatkan installer terbaru

Installer tidak disimpan di repository karena ukurannya besar. Unduh installer dari halaman [Releases](https://github.com/yahya06/pdf-safetools/releases). Folder `build\`, `dist\`, dan `scripts\dist\` adalah artefak lokal dan diabaikan oleh Git.

---

## Penggunaan

1. Buka PDF SafeTools.
2. Pilih fitur dari sidebar: Merge, Split, Compress, Scan, atau Sanitize.
3. Tambahkan file PDF (drag & drop atau tombol Add).
4. Jalankan operasi.
5. Output disimpan ke folder output (default: `%LOCALAPPDATA%\PDFSafeTools\output`).

File original tidak pernah diubah. Output otomatis diberi suffix:

```
original.pdf       → original_clean.pdf
original.pdf       → original_compressed.pdf
merge multiple     → merged.pdf
```

---

## PDF Scanner

Scanner melakukan analisis statis terhadap struktur PDF. Scanner tidak menjalankan JavaScript atau action PDF.

Mendeteksi:

```
/JavaScript   /JS            /OpenAction    /AA
/URI          /Launch        /GoToR         /GoToE
/EmbeddedFiles /SubmitForm   /ImportData    /RichMedia
/Movie        /Sound         /3D
```

Severity: `INFO` `LOW` `MEDIUM` `HIGH` `CRITICAL`

---

## PDF Sanitizer

Sanitizer menghapus object dan action PDF yang berisiko:

- JavaScript
- OpenAction
- Additional Actions (AA)
- External URI
- Launch
- GoToR / GoToE
- SubmitForm / ImportData
- Embedded Files
- RichMedia / Movie / Sound / 3D
- Dangerous annotations
- Optional metadata cleaning

### Preset

| Preset | Ringkasan |
|---|---|
| Standard | JavaScript, OpenAction, External URI, Launch, Embedded Files |
| JKN Safe Mode | Semua rule aktif |
| Custom | Pilih rule secara manual |

### Alur sanitasi

```
Original → Scan → Sanitize → Save → Re-scan → Final Report
```

Hasil sanitasi selalu diverifikasi ulang dengan re-scan.

> **Catatan:** `JKN Safe Mode` adalah nama preset konfigurasi sanitasi berdasarkan kebutuhan project. Bukan spesifikasi atau rekomendasi resmi JKN.

---

## Keamanan & Privasi

- Semua pemrosesan PDF bersifat lokal.
- PDF tidak pernah dikirim ke server eksternal.
- Log tidak menyimpan konten PDF, data pasien, atau password.
- SHA-256 dihitung untuk identifikasi dan audit lokal.
- Hash tidak dikirim ke server eksternal.
- Aplikasi data disimpan di `%LOCALAPPDATA%\PDFSafeTools\`.

### Disclaimer keamanan

PDF SafeTools tidak menjamin sebuah PDF:

- Bebas dari seluruh jenis malware.
- Aman secara absolut.
- Tidak mengandung vulnerability.
- Pasti diterima oleh sistem tertentu.

Istilah `SAFE` hanya status aplikasi berdasarkan rule scanner yang aktif. Bukan jaminan bebas malware.

Untuk hasil scan bersih, gunakan istilah:

```
No configured findings detected
```

---

## Development

### Menjalankan test

```powershell
pytest
```

### Lint & format

```powershell
ruff check .
ruff format .
```

### Type check

```powershell
mypy app/
```

### Urutan verifikasi

```powershell
ruff check .
ruff format .
mypy app/
pytest
```

### Build executable

PyInstaller build tersedia melalui `scripts/build.py`:

```powershell
.venv\Scripts\python.exe scripts\build.py --clean
```

Output berada di `dist\PDFSafeTools\PDFSafeTools.exe`. Untuk membuat installer Inno Setup, pastikan Inno Setup terpasang dan compiler `iscc` tersedia di `PATH`, lalu jalankan:

```powershell
.venv\Scripts\python.exe scripts\build.py --clean --installer
```

Installer dibuat di `scripts\dist\installer\PDFSafeTools-Setup.exe`. Jangan commit hasil build; unggah installer ke halaman GitHub Releases. Ghostscript tetap harus dipasang terpisah untuk fitur compression.

---

## Kontribusi

Kontribusi diterima. Lihat `CONTRIBUTING.md` untuk panduan kontribusi (akan ditambahkan).
2. Jalankan test, lint, dan type check.
3. Jangan commit data pasien, dokumen rumah sakit, credential, atau production log.
4. Untuk fixture PDF, gunakan PDF sintetis — bukan dokumen nyata.

---

## Security Policy

Jika menemukan vulnerability, laporkan secara privat ke maintainer. Jangan membuka GitHub issue publik untuk laporan security.

Jangan mengunggah:
- File PDF yang mengandung data pasien.
- Rekam medis.
- Dokumen internal rumah sakit.

Detail lihat `SECURITY.md` (jika sudah tersedia).

---

## Project Origin

Project ini dikembangkan berdasarkan kebutuhan teknis pengolahan dokumen PDF di lingkungan kerja:

```
RSUD Bantarangin Ponorogo
Ponorogo, Jawa Timur, Indonesia
```

### Disclaimer

PDF SafeTools:

- **Bukan** aplikasi resmi RSUD Bantarangin Ponorogo.
- **Bukan** produk resmi JKN.
- **Bukan** produk resmi BPJS Kesehatan.
- **Bukan** produk resmi Kementerian Kesehatan Republik Indonesia.

Nama institusi digunakan untuk menjelaskan asal kebutuhan dan konteks pengembangan project.

---

## Developer

**Yahya**

GitHub: [https://github.com/yahya06](https://github.com/yahya06)

Repository: [https://github.com/yahya06/pdf-safetools](https://github.com/yahya06/pdf-safetools)

---

## Tech Stack

| Komponen | Teknologi |
|---|---|
| Bahasa | Python 3.12+ |
| GUI | PySide6 |
| PDF manipulation | pikepdf |
| PDF rendering | PyMuPDF |
| Compression | Ghostscript |
| Packaging | PyInstaller |
| Platform | Windows Desktop |

---

## License

License ditentukan sebelum public release. Lihat file `LICENSE`.

---

## Links

| Link | URL |
|---|---|
| Developer GitHub | https://github.com/yahya06 |
| Repository | https://github.com/yahya06/pdf-safetools |
| Releases | https://github.com/yahya06/pdf-safetools/releases |
