# PDF SafeTools

**PDF Utility & Security Tool for Windows**

> Merge • Split • Compress • Organize • Scan • Sanitize

---

# 1. Project Overview

**PDF SafeTools** adalah aplikasi desktop Windows untuk melakukan pengolahan,
pemeriksaan, dan sanitasi dokumen PDF secara lokal.

Project ini dikembangkan berdasarkan kebutuhan teknis pengolahan dokumen PDF
di lingkungan kerja **RSUD Bantarangin Ponorogo**, Jawa Timur, Indonesia.

Aplikasi dirancang untuk digunakan pada PC tertentu dan tidak membutuhkan
server web, database, atau koneksi internet untuk melakukan operasi PDF utama.

---

# 2. Project Origin

## Developed At

**RSUD Bantarangin Ponorogo**  
Ponorogo, Jawa Timur, Indonesia

## Project Type

Open Source / Community Project

## Primary Platform

Windows Desktop

## Development Approach

- Local-first
- Privacy-first
- Security-oriented
- Offline-capable

## Background

Project ini dibuat berdasarkan kebutuhan pengolahan dokumen PDF, termasuk
dokumen yang akan digunakan atau diunggah ke sistem lain.

Salah satu perhatian utama adalah adanya PDF yang mengandung object, action,
atau resource tertentu yang dapat menyebabkan dokumen dianggap mencurigakan
oleh sistem keamanan.

PDF SafeTools dikembangkan untuk menyediakan tool lokal yang dapat:

- Menggabungkan PDF.
- Memisahkan PDF.
- Mengatur halaman PDF.
- Mengompres PDF.
- Mengkonversi PDF dan image.
- Memeriksa struktur PDF.
- Mendeteksi PDF action tertentu.
- Membersihkan object/action PDF tertentu.
- Melakukan re-scan setelah sanitasi.
- Menghasilkan laporan hasil pemeriksaan.

---

# 3. Important Disclaimer

PDF SafeTools merupakan project open-source yang dikembangkan berdasarkan
kebutuhan teknis pengolahan dokumen PDF.

Project ini:

- **Bukan aplikasi resmi RSUD Bantarangin Ponorogo.**
- **Bukan produk resmi JKN.**
- **Bukan produk resmi BPJS Kesehatan.**
- **Bukan produk resmi Kementerian Kesehatan Republik Indonesia.**
- Tidak mengklaim sebagai tool keamanan resmi dari institusi mana pun.

Nama **RSUD Bantarangin Ponorogo** digunakan untuk menjelaskan asal kebutuhan
dan konteks pengembangan project.

Pencantuman institusi tersebut tidak berarti bahwa project ini secara otomatis
didukung, disponsori, disahkan, atau dikelola secara resmi oleh institusi
tersebut.

---

# 4. Security Disclaimer

PDF SafeTools tidak menjamin bahwa sebuah PDF:

- Bebas dari seluruh jenis malware.
- Aman secara absolut.
- Tidak mengandung vulnerability.
- Pasti diterima oleh sistem tertentu.
- Pasti lolos proses validasi JKN.
- Pasti lolos seluruh antivirus atau security scanner.

Sanitasi hanya dilakukan terhadap object, action, dan struktur PDF yang
termasuk dalam rule sanitasi yang diimplementasikan oleh versi aplikasi.

Istilah `SAFE` tidak boleh digunakan untuk menyatakan bahwa file terbukti
bebas malware.

Untuk hasil scanner yang bersih gunakan istilah:

```text
No configured dangerous PDF actions detected
```

atau:

```text
No configured findings detected
```

---

# 5. Main Goals

Tujuan project:

1. Menyediakan PDF utility desktop untuk Windows.
2. Menyediakan PDF security scanner.
3. Menyediakan PDF sanitizer.
4. Membantu membersihkan PDF yang mengandung action/object yang tidak diperlukan.
5. Menjaga dokumen tetap berada di komputer lokal.
6. Mengurangi ketergantungan terhadap online PDF tools.
7. Menyediakan aplikasi yang dapat digunakan tanpa server.
8. Menjadi project open-source yang dapat dikembangkan bersama.

---

# 6. Target Platform

Target utama:

```text
Windows 10
Windows 11
x64
```

Tidak menjadi target utama:

```text
Linux
macOS
Android
iOS
Web
```

Arsitektur harus tetap memungkinkan porting di masa depan, tetapi kompatibilitas
Windows adalah prioritas utama.

---

# 7. Technology Stack

## Programming Language

```text
Python 3.12+
```

Versi Python harus dikunci ketika release untuk menjaga reproducibility.

## GUI

```text
PySide6
```

PySide6 digunakan untuk seluruh desktop interface.

Tidak menggunakan:

```text
Laravel
PHP
Electron
React
Next.js
Browser-based UI
```

kecuali ada keputusan arsitektur baru yang terdokumentasi.

---

# 8. PDF Processing Stack

## pikepdf

Digunakan untuk:

- PDF object manipulation.
- PDF structure.
- PDF action.
- JavaScript.
- Embedded files.
- PDF sanitization.

Repository resmi:

```text
https://github.com/pikepdf/pikepdf
```

## PyMuPDF

Digunakan untuk:

- PDF rendering.
- Page preview.
- Page extraction.
- Rotation.
- PDF information.
- PDF → image.
- Image-related operations.

Package:

```text
PyMuPDF
```

## Ghostscript

Digunakan terutama untuk:

- PDF compression.
- Image downsampling.
- PDF optimization.
- PDF rewriting tertentu.

Ghostscript diperlakukan sebagai external executable.

Jangan hardcode versi.

---

# 9. PDF Sanitizer Reference

Referensi utama sanitasi:

```text
https://github.com/krisnadwiki/PDF-Sanitizer
```

Repository tersebut menjadi referensi teknis untuk pengembangan sanitasi PDF.

Implementasi harus memperhatikan:

- License.
- Copyright.
- Attribution.
- Dependency license.
- Perbedaan kebutuhan project.

Jangan melakukan copy-paste seluruh repository tanpa memahami license dan
implikasinya.

Logic sanitasi harus dibuat modular agar mudah diaudit dan diuji.

---

# 10. Privacy Principle

PDF SafeTools menerapkan prinsip:

```text
LOCAL FIRST
PRIVACY FIRST
NO CLOUD
```

Dokumen PDF diproses secara lokal.

Aplikasi tidak boleh secara otomatis:

- Upload PDF ke cloud.
- Mengirim PDF ke API pihak ketiga.
- Mengirim PDF ke AI.
- Mengirim PDF ke online malware scanner.
- Mengirim dokumen pasien ke server eksternal.

Operasi PDF utama harus tetap berjalan tanpa koneksi internet.

---

# 11. Sensitive Data

PDF dapat mengandung informasi sensitif, termasuk informasi kesehatan.

Karena itu:

```text
PDF = Sensitive Data
```

Secara default aplikasi harus memperlakukan file PDF sebagai data sensitif.

Jangan menyimpan:

- Isi PDF di log.
- Screenshot PDF secara otomatis.
- Password PDF.
- Data pasien dalam telemetry.
- Metadata dokumen ke server eksternal.

---

# 12. Architecture

```text
┌──────────────────────────────────────────────┐
│                 PDF SafeTools               │
│                                              │
│                 PySide6 GUI                  │
│                       │                      │
│        ┌──────────────┼──────────────┐       │
│        │              │              │       │
│        ▼              ▼              ▼       │
│    PDF Tools      Security        Settings   │
│        │              │                      │
│        │              ▼                      │
│        │         PDF Scanner                 │
│        │              │                      │
│        │              ▼                      │
│        │         PDF Sanitizer               │
│        │              │                      │
│        └──────────────┼──────────────────────┘
│                       │
│                       ▼
│               PDF Processing Layer
│                       │
│          ┌────────────┼────────────┐
│          ▼            ▼            ▼
│       pikepdf       PyMuPDF    Ghostscript
│                                              │
└──────────────────────────────────────────────┘
```

---

# 13. Project Structure

```text
pdf-safetools/
│
├── app/
│   ├── main.py
│   │
│   ├── ui/
│   │   ├── main_window.py
│   │   ├── dashboard.py
│   │   ├── merge_page.py
│   │   ├── split_page.py
│   │   ├── compress_page.py
│   │   ├── organize_page.py
│   │   ├── scan_page.py
│   │   ├── sanitize_page.py
│   │   ├── settings_page.py
│   │   └── about_page.py
│   │
│   ├── services/
│   │   ├── pdf_service.py
│   │   ├── merge_service.py
│   │   ├── split_service.py
│   │   ├── compress_service.py
│   │   ├── organize_service.py
│   │   ├── render_service.py
│   │   ├── scanner_service.py
│   │   └── sanitizer_service.py
│   │
│   ├── security/
│   │   ├── scanner.py
│   │   ├── sanitizer.py
│   │   ├── findings.py
│   │   └── rules.py
│   │
│   ├── models/
│   │   ├── scan_result.py
│   │   ├── sanitize_result.py
│   │   └── pdf_info.py
│   │
│   ├── workers/
│   │   ├── pdf_worker.py
│   │   ├── scan_worker.py
│   │   └── sanitize_worker.py
│   │
│   ├── utils/
│   │   ├── file_utils.py
│   │   ├── hash_utils.py
│   │   ├── logging_utils.py
│   │   └── system_utils.py
│   │
│   └── config/
│       └── settings.py
│
├── assets/
│   ├── icons/
│   ├── images/
│   └── styles/
│
├── tests/
│   ├── test_merge.py
│   ├── test_split.py
│   ├── test_compress.py
│   ├── test_scanner.py
│   └── test_sanitizer.py
│
├── sample_pdfs/
│   ├── safe/
│   ├── javascript/
│   ├── external_uri/
│   ├── open_action/
│   ├── launch/
│   ├── embedded/
│   ├── annotation/
│   ├── multimedia/
│   ├── encrypted/
│   └── malformed/
│
├── scripts/
│   ├── build.py
│   └── package.py
│
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
├── PROJECT.md
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
└── LICENSE
```

---

# 14. Application UI

Main layout:

```text
┌────────────────────────────────────────────────────┐
│ PDF SafeTools                                      │
├──────────────┬─────────────────────────────────────┤
│ Dashboard    │                                     │
│              │          Content Area               │
│ PDF Tools    │                                     │
│  Merge       │                                     │
│  Split       │                                     │
│  Compress    │                                     │
│  Organize    │                                     │
│              │                                     │
│ Security     │                                     │
│  Scan        │                                     │
│  Sanitize    │                                     │
│              │                                     │
│ Settings     │                                     │
│ About        │                                     │
└──────────────┴─────────────────────────────────────┘
```

Gunakan sidebar navigation.

---

# 15. PDF Tools

MVP harus menyediakan:

```text
Merge PDF
Split PDF
Rotate PDF
Delete Page
Reorder Page
Extract Page
Compress PDF
PDF → Image
Image → PDF
PDF Information
```

---

# 16. Merge PDF

Fitur:

- Drag & drop.
- Add PDF.
- Remove PDF.
- Clear list.
- Reorder.
- Merge.
- Save output.

Workflow:

```text
Add PDF
   ↓
Validate PDF
   ↓
Display files
   ↓
Reorder
   ↓
Merge
   ↓
Save output
```

Original file tidak boleh diubah.

---

# 17. Split PDF

Mendukung:

```text
All pages
Page range
Selected pages
Every N pages
```

Contoh:

```text
1-3
5
8-10
```

Output:

```text
output/
├── document_001.pdf
├── document_002.pdf
└── document_003.pdf
```

---

# 18. Organize PDF

Mendukung:

- Page preview.
- Thumbnail.
- Drag & drop reorder.
- Rotate.
- Delete.
- Extract.

---

# 19. Compress PDF

Preset:

```text
Low
Medium
High
Custom
```

Tampilkan:

```text
Original Size
Output Size
Reduction Percentage
```

Jangan mengklaim compression selalu lossless.

---

# 20. PDF Scanner

Scanner hanya melakukan analisis statis.

Scanner **tidak boleh menjalankan JavaScript atau action PDF**.

Minimal mendeteksi:

```text
/JavaScript
/JS
/OpenAction
/AA
/URI
/Launch
/GoToR
/GoToE
/EmbeddedFiles
/SubmitForm
/ImportData
/RichMedia
/Movie
/Sound
/3D
```

---

# 21. Security Finding

Format:

```python
{
    "type": "external_uri",
    "severity": "HIGH",
    "count": 3,
    "description": "External URI action detected",
    "action": "REMOVE",
}
```

---

# 22. Severity

Gunakan:

```text
INFO
LOW
MEDIUM
HIGH
CRITICAL
```

Contoh:

```text
JavaScript       CRITICAL
Launch           HIGH
External URI     HIGH
Embedded File    HIGH
OpenAction       HIGH
Metadata         INFO
```

Severity harus configurable.

---

# 23. Risk Level

Gunakan:

```text
SAFE
LOW
MEDIUM
HIGH
CRITICAL
```

Namun `SAFE` hanya boleh digunakan sebagai status aplikasi berdasarkan rule
scanner yang aktif.

Tidak boleh diartikan sebagai jaminan bebas malware.

---

# 24. PDF Sanitizer

Sanitizer modular:

```text
sanitize_pdf()
│
├── remove_javascript()
├── remove_open_action()
├── remove_additional_actions()
├── remove_external_access()
├── remove_launch_actions()
├── remove_embedded_files()
├── remove_rich_media()
├── remove_multimedia()
├── remove_dangerous_annotations()
└── clean_metadata()
```

---

# 25. Sanitization Presets

## Standard

```text
JavaScript
OpenAction
External URI
Launch
Embedded Files
```

## JKN Safe Mode

```text
JavaScript
OpenAction
AA
External URI
Launch
GoToR
GoToE
SubmitForm
ImportData
Embedded Files
RichMedia
Movie
Sound
3D
Dangerous annotations
```

## Custom

User dapat memilih rule secara manual.

> **Catatan:** `JKN Safe Mode` adalah nama preset konfigurasi sanitasi
> berdasarkan kebutuhan project. Nama tersebut tidak berarti preset ini
> merupakan spesifikasi resmi atau rekomendasi resmi JKN.

---

# 26. Important Sanitization Rule

Jangan hanya mencari:

```text
http://
https://
www.
```

dan menghapusnya.

URL yang tercetak sebagai teks biasa pada halaman PDF tidak otomatis berbahaya.

Sanitizer harus fokus pada PDF object/action seperti:

```text
/URI
/Launch
/GoToR
/GoToE
/SubmitForm
/ImportData
```

---

# 27. JavaScript

Deteksi:

```text
/JavaScript
/JS
```

Action:

```text
REMOVE
```

JavaScript PDF tidak boleh dijalankan oleh scanner.

---

# 28. OpenAction

Deteksi:

```text
/OpenAction
```

Jika termasuk action yang tidak diperlukan atau berisiko:

```text
REMOVE
```

---

# 29. Additional Actions

Deteksi:

```text
/AA
```

Periksa action terkait.

Sanitizer harus menangani action yang dapat menyebabkan perilaku eksternal.

---

# 30. External Access

Deteksi:

```text
/URI
/Launch
/GoToR
/GoToE
/SubmitForm
/ImportData
```

Default JKN Safe Mode:

```text
REMOVE
```

---

# 31. Embedded Files

Deteksi:

```text
/EmbeddedFiles
```

JKN Safe Mode:

```text
REMOVE
```

Tampilkan jumlah embedded file yang dihapus jika memungkinkan.

---

# 32. Multimedia

Deteksi:

```text
/RichMedia
/Movie
/Sound
/3D
```

JKN Safe Mode:

```text
REMOVE
```

---

# 33. Annotation

Deteksi:

```text
/Annot
```

Prioritaskan annotation yang berhubungan dengan external access.

Default:

```text
Remove external link annotations = ON
Remove all annotations = OFF
```

Jangan menghapus seluruh annotation secara default.

---

# 34. Metadata

Optional:

```text
Author
Creator
Producer
Title
Subject
Keywords
CreationDate
ModDate
```

Metadata cleaning tidak boleh menjadi default jika dapat mengganggu kebutuhan
dokumen.

---

# 35. Re-scan

Sanitization wajib mengikuti:

```text
Original
   ↓
Scan
   ↓
Sanitize
   ↓
Save
   ↓
Re-scan
   ↓
Final Report
```

Hasil sanitasi harus selalu diverifikasi ulang.

---

# 36. Original File Protection

Default:

```text
Never overwrite original
```

Contoh:

```text
original.pdf
      ↓
original_clean.pdf
```

Overwrite hanya jika user secara eksplisit memilihnya.

---

# 37. SHA-256

Hitung:

```text
SHA-256 Original
SHA-256 Output
```

Digunakan untuk:

- Identifikasi.
- Audit lokal.
- Debugging.
- Verifikasi perubahan.

Hash tidak boleh dikirim ke server eksternal.

---

# 38. Temporary Files

Gunakan:

```text
%LOCALAPPDATA%\PDFSafeTools\temp
```

Temporary files harus dibersihkan setelah proses.

Jika gagal dihapus, tulis warning ke log.

---

# 39. Application Data

Gunakan:

```text
%LOCALAPPDATA%\PDFSafeTools\
```

Struktur:

```text
PDFSafeTools/
├── logs/
├── temp/
├── output/
├── config/
└── cache/
```

Jangan menyimpan application data di:

```text
C:\Program Files\
```

---

# 40. Logging

Gunakan rotating log.

Contoh:

```text
logs/app.log
```

Log:

```text
INFO
WARNING
ERROR
```

Jangan memasukkan:

```text
PDF content
Patient data
PDF password
Image content
```

ke dalam log.

Jika filename mengandung informasi sensitif, masking dapat diterapkan.

---

# 41. Threading

Operasi PDF tidak boleh membuat UI freeze.

Gunakan mekanisme PySide6:

```text
QThread
QRunnable
QThreadPool
```

atau implementasi worker yang sesuai.

---

# 42. Progress

Operasi panjang harus menampilkan progress jika progress dapat dihitung.

Contoh:

```text
Scanning...
████████████░░░░ 75%

Sanitizing...
██████████████░░ 85%
```

Jika tidak dapat dihitung secara akurat:

```text
Processing...
```

Jangan membuat progress palsu.

---

# 43. Error Handling

User-facing error harus sederhana.

Contoh:

```text
Tidak dapat membuka PDF.

Kemungkinan penyebab:
• File rusak
• File terenkripsi
• File bukan PDF valid
• Format PDF tidak didukung
```

Traceback hanya disimpan ke log.

---

# 44. Password PDF

Jika PDF terenkripsi:

```text
PDF is encrypted.
```

Jika memungkinkan:

```text
[ Enter Password ]
```

Password:

- Tidak disimpan.
- Tidak ditulis ke log.
- Hanya berada di memory selama proses.

---

# 45. Batch Processing

Dirancang untuk mendukung:

```text
Add Folder
Scan All
Sanitize All
Compress All
```

Output:

```text
output/
├── 001_clean.pdf
├── 002_clean.pdf
├── 003_clean.pdf
└── 004_clean.pdf
```

Batch processing dapat masuk setelah MVP.

---

# 46. Drag & Drop

Support:

```text
Windows Explorer
      ↓
PDF SafeTools
```

Untuk:

```text
PDF
Image
Folder
```

Folder processing dapat diaktifkan pada tahap batch.

---

# 47. Output Naming

Default:

```text
original.pdf
→
original_clean.pdf
```

Compression:

```text
original.pdf
→
original_compressed.pdf
```

Merge:

```text
merged.pdf
```

User dapat mengganti nama output.

---

# 48. Settings

Minimal:

```text
Output folder
Temporary folder
Default compression
Default sanitizer preset
Ghostscript path
Theme
Language
Auto cleanup
```

---

# 49. Theme

MVP:

```text
Light
Dark
System
```

Gunakan Qt stylesheet.

---

# 50. About

Halaman About menampilkan informasi aplikasi, developer, dan asal project.

Contoh:

```text
┌──────────────────────────────────────────────────┐
│                                                  │
│                 PDF SafeTools                   │
│                                                  │
│           PDF Utility & Security Tool            │
│                                                  │
│                   Version 1.0.0                  │
│                                                  │
│ ──────────────────────────────────────────────── │
│                                                  │
│ Developer                                        │
│                                                  │
│ Yahya                                            │
│                                                  │
│              [ GitHub Profile ↗ ]                │
│                                                  │
│ ──────────────────────────────────────────────── │
│                                                  │
│ Project Origin                                   │
│                                                  │
│ RSUD Bantarangin Ponorogo                       │
│ Ponorogo, Jawa Timur, Indonesia                  │
│                                                  │
│ Developed based on technical needs at            │
│ RSUD Bantarangin Ponorogo.                      │
│                                                  │
│ ──────────────────────────────────────────────── │
│                                                  │
│ 🔒 Local Processing                              │
│ ☁ No Cloud Upload                               │
│ 🛡 Privacy First                                 │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

# 50.1 Developer Information

Developer:

```text
Yahya
```

GitHub Profile:

```text
https://github.com/yahya06
```

UI:

```text
Developed by

Yahya

[ GitHub Profile ↗ ]
```

Tombol **GitHub Profile** membuka profile GitHub menggunakan default browser
Windows.

Implementasi PySide6:

```python
import webbrowser

webbrowser.open("https://github.com/yahya06")
```

Jangan menggunakan embedded browser hanya untuk membuka profile GitHub.

---

# 50.2 Project Origin

Tampilkan:

```text
Project Origin

RSUD Bantarangin Ponorogo
Ponorogo, Jawa Timur, Indonesia
```

Keterangan:

```text
Developed based on technical needs at
RSUD Bantarangin Ponorogo.
```

Informasi ini hanya menunjukkan **asal kebutuhan dan konteks pengembangan**
project.

Project bukan aplikasi resmi:

- RSUD Bantarangin Ponorogo
- JKN
- BPJS Kesehatan
- Kementerian Kesehatan Republik Indonesia

kecuali dinyatakan secara resmi pada masa mendatang.

---

# 50.3 Application Footer

Footer aplikasi:

```text
PDF SafeTools v1.0.0
Developed by Yahya · GitHub
Project Origin: RSUD Bantarangin Ponorogo
```

`GitHub` merupakan clickable link menuju:

```text
https://github.com/yahya06
```

Footer tidak perlu menampilkan URL panjang.

---

# 50.4 External Links

External link yang digunakan pada versi awal:

| Link | URL | Status |
|---|---|---|
| Developer GitHub | https://github.com/yahya06 | Aktif |
| Project Repository | https://github.com/yahya06/pdf-safetools.git | Aktif |
| Documentation | - | Belum dibuat |
| Security Policy | - | Akan tersedia di repository |

Project Repository **jangan dibuat sebagai link sementara**.

Setelah repository dibuat, URL repository dapat ditambahkan ke konfigurasi
aplikasi.

Semua external link hanya dibuka setelah user melakukan aksi seperti:

```text
Click GitHub Profile
Click Project Repository
Click Documentation
```

Aplikasi tidak boleh melakukan koneksi otomatis ke link tersebut ketika
aplikasi dijalankan.

---

# 50.5 Configurable Developer Profile

Informasi developer dan project tidak boleh tersebar di banyak file.

Gunakan konfigurasi terpusat:

```python
APP_INFO = {
    "name": "PDF SafeTools",
    "developer": "Yahya",
    "github_profile": "https://github.com/yahya06",
    "repository": None,
    "institution": "RSUD Bantarangin Ponorogo",
    "location": "Ponorogo, Jawa Timur, Indonesia",
}
```

Ketika repository GitHub sudah dibuat:

```python
APP_INFO = {
    "name": "PDF SafeTools",
    "developer": "Yahya",
    "github_profile": "https://github.com/yahya06",
    "repository": "https://github.com/yahya06/pdf-safetools",
    "institution": "RSUD Bantarangin Ponorogo",
    "location": "Ponorogo, Jawa Timur, Indonesia",
}
```

UI harus menyembunyikan tombol **Project Repository** apabila:

```python
repository is None
```

Dengan demikian aplikasi versi awal tidak memiliki link mati.

---

# 51. File Validation

Jangan hanya memeriksa extension.

Validasi:

```text
Extension
PDF signature
PDF parser
```

Header PDF:

```text
%PDF-
```

---

# 52. Process Security

Jangan menggunakan:

```python
os.system(...)
```

dengan input user.

Jangan menggunakan:

```python
subprocess.run(command, shell=True)
```

dengan data user.

Gunakan argument list:

```python
subprocess.run(
    [
        executable,
        "-option",
        input_file,
        output_file,
    ],
    check=True,
)
```

---

# 53. Ghostscript Security

Ghostscript harus dijalankan dengan konfigurasi yang aman.

Jangan memberikan permission atau option yang tidak diperlukan.

Path executable harus divalidasi.

---

# 54. Static Scanner

Scanner tidak boleh mengeksekusi:

```text
JavaScript
Embedded executable
External URL
Launch action
```

Scanner hanya membaca struktur PDF.

---

# 55. Deterministic Sanitizer

Dengan:

```text
input.pdf
+
preset
```

hasil sanitasi harus konsisten.

Hindari randomness yang tidak diperlukan.

---

# 56. Testing

Gunakan:

```text
pytest
pytest-qt
```

Test minimal:

```text
Normal PDF
JavaScript PDF
External URI PDF
OpenAction PDF
Launch PDF
Embedded File PDF
Annotation PDF
Malformed PDF
Encrypted PDF
Fake PDF
```

---

# 57. Security Test Fixtures

Gunakan PDF fixture yang aman untuk testing.

Jangan memasukkan malware aktif ke repository.

Contoh:

```text
sample_pdfs/
├── safe/
├── javascript/
├── external_uri/
├── open_action/
├── launch/
├── embedded/
├── annotation/
├── multimedia/
├── encrypted/
└── malformed/
```

---

# 58. Regression Testing

Setiap security bug harus menjadi regression test.

Workflow:

```text
Bug ditemukan
     ↓
Buat fixture
     ↓
Implement fix
     ↓
Tambah test
     ↓
Run test
```

Bug yang sudah diperbaiki tidak boleh muncul kembali.

---

# 59. Development Environment

Requirement:

```text
Windows 10/11
Python 3.12+
Git
Ghostscript
```

Create virtual environment:

```powershell
python -m venv .venv
```

Activate:

```powershell
.venv\Scripts\Activate.ps1
```

Install:

```powershell
pip install -r requirements.txt
```

Run:

```powershell
python -m app.main
```

---

# 60. Code Quality

Gunakan:

```text
PEP 8
Type hints
Docstrings
Small functions
Single responsibility
```

Hindari:

```text
God class
God function
Global mutable state
Hardcoded paths
shell=True
Duplicate logic
```

Development tools:

```text
ruff
black
mypy
pytest
```

---

# 61. AI Coding Agent Rules

Project ini dikembangkan menggunakan AI coding agent seperti:

- Codex
- OpenCode
- Cline
- GitHub Copilot

AI agent wajib:

1. Membaca `PROJECT.md`.
2. Membaca `README.md`.
3. Memeriksa struktur repository.
4. Memahami existing code.
5. Membuat rencana sebelum perubahan besar.
6. Mengubah kode secara minimal dan terarah.
7. Tidak mengganti framework.
8. Tidak mengganti library utama tanpa alasan.
9. Tidak menambahkan dependency yang tidak diperlukan.
10. Membuat test untuk fitur baru.
11. Menjalankan test setelah perubahan.
12. Memperbaiki error sebelum melanjutkan.
13. Tidak menghapus test existing.
14. Tidak menghapus fitur existing.
15. Tidak mengubah behavior existing tanpa alasan.
16. Memastikan kompatibilitas Windows.
17. Tidak menggunakan Docker untuk runtime aplikasi.
18. Tidak menggunakan WSL untuk runtime aplikasi.
19. Tidak membutuhkan internet untuk PDF processing.
20. Tidak mengirim dokumen keluar komputer.

---

# 62. AI Task Workflow

Setiap task:

```text
READ
 ↓
ANALYZE
 ↓
PLAN
 ↓
IMPLEMENT
 ↓
TEST
 ↓
VERIFY
 ↓
REPORT
```

AI harus melaporkan:

```text
Changed:
- ...

Added:
- ...

Tests:
- ...

Result:
PASS / FAIL

Potential Issues:
- ...
```

---

# 63. Development Philosophy

Jangan overengineering.

MVP tidak membutuhkan:

```text
Database
Authentication
Web Server
REST API
Cloud Storage
Microservices
Docker
```

Aplikasi adalah:

```text
Windows Desktop Application
```

---

# 64. MVP Scope

MVP:

```text
[ ] PySide6 GUI
[ ] Merge PDF
[ ] Split PDF
[ ] Rotate PDF
[ ] Delete Page
[ ] Reorder Page
[ ] Compress PDF
[ ] PDF → Image
[ ] Image → PDF
[ ] PDF Information
[ ] Scan PDF
[ ] Sanitize PDF
[ ] JKN Safe Mode
[ ] Security Report
[ ] Re-scan Output
[ ] Drag & Drop
[ ] Local Processing
[ ] Temporary Cleanup
[ ] Logging
```

Tidak termasuk MVP:

```text
[ ] OCR
[ ] User Account
[ ] Cloud Storage
[ ] Database
[ ] AI Processing
```

---

# 65. Development Phases

## Phase 1 — Foundation

- [ ] Project setup.
- [ ] PySide6.
- [ ] Main Window.
- [ ] Sidebar.
- [ ] Dashboard.
- [ ] Settings.
- [ ] About.
- [ ] Logging.

## Phase 2 — PDF Core

- [ ] PDF validation.
- [ ] PDF information.
- [ ] Merge.
- [ ] Split.
- [ ] Rotate.
- [ ] Delete page.
- [ ] Reorder.
- [ ] PDF → Image.
- [ ] Image → PDF.

## Phase 3 — Compression

- [ ] Ghostscript integration.
- [ ] Compression presets.
- [ ] Output comparison.
- [ ] Progress.
- [ ] Error handling.

## Phase 4 — Security Scanner

- [ ] Static PDF parser.
- [ ] JavaScript detection.
- [ ] OpenAction detection.
- [ ] AA detection.
- [ ] URI detection.
- [ ] Launch detection.
- [ ] GoToR detection.
- [ ] GoToE detection.
- [ ] Embedded file detection.
- [ ] Multimedia detection.
- [ ] Annotation detection.
- [ ] Risk calculation.
- [ ] Security report.

## Phase 5 — Sanitizer

- [ ] JavaScript removal.
- [ ] OpenAction removal.
- [ ] AA removal.
- [ ] External URI removal.
- [ ] Launch removal.
- [ ] GoToR removal.
- [ ] GoToE removal.
- [ ] Embedded file removal.
- [ ] Multimedia removal.
- [ ] Dangerous annotation removal.
- [ ] Optional metadata cleaning.

## Phase 6 — JKN Safe Mode

- [ ] JKN preset.
- [ ] Test fixtures.
- [ ] Real-world problematic PDF testing.
- [ ] Regression tests.
- [ ] Re-scan.
- [ ] Sanitization report.

## Phase 7 — Batch

- [ ] Folder processing.
- [ ] Batch scan.
- [ ] Batch sanitize.
- [ ] Batch compression.
- [ ] Progress queue.

## Phase 8 — Packaging

- [ ] PyInstaller.
- [ ] Windows executable.
- [ ] Installer.
- [ ] Application icon.
- [ ] Version information.
- [ ] Dependency verification.
- [ ] Clean Windows testing.

---

# 66. Packaging

Gunakan:

```text
PyInstaller
```

Target:

```text
Windows x64
```

Output:

```text
PDFSafeTools.exe
```

Production installer:

```text
PDFSafeTools-Setup.exe
```

User akhir tidak perlu menginstall:

```text
Python
pip
Git
```

---

# 67. Portable Version

Future release dapat menyediakan:

```text
PDFSafeTools-Portable.zip
```

Contoh:

```text
PDFSafeTools/
├── PDFSafeTools.exe
├── runtime/
├── config/
└── README.txt
```

Portable version tidak boleh membutuhkan Python terinstall.

---

# 68. GitHub Repository

Repository public disarankan menggunakan nama:

```text
pdf-safetools
```

Developer:

```text
Yahya
```

GitHub Profile:

```text
https://github.com/yahya06
```

Repository:

```text
https://github.com/yahya06/pdf-safetools.git
```

Hindari nama repository:

```text
rsud-bantarangin-pdf
jkn-pdf-tool
official-jkn-pdf
```

agar tidak memberikan kesan sebagai aplikasi resmi institusi atau JKN.

---

# 69. Public Repository Structure

```text
pdf-safetools/
│
├── .github/
│   ├── workflows/
│   │   ├── tests.yml
│   │   └── build-windows.yml
│   └── ISSUE_TEMPLATE/
│
├── app/
├── assets/
├── tests/
├── sample_pdfs/
├── scripts/
│
├── .gitignore
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── PROJECT.md
├── README.md
├── SECURITY.md
├── requirements.txt
├── requirements-dev.txt
└── pyproject.toml
```

---

# 70. Git Ignore

Repository tidak boleh menyimpan:

```text
.env
*.pdf
*.bak
*.db
*.sqlite
*.log
*.tmp
patient_data/
medical_records/
credentials/
passwords/
private_keys/
certificates/
```

Gunakan `.gitignore`.

---

# 71. Sensitive Data Policy

Jangan commit:

```text
Data pasien
Rekam medis
Dokumen internal rumah sakit
Screenshot sistem internal
Credential
Password
API key
Private certificate
Production log
```

Jika membutuhkan contoh PDF untuk testing, gunakan fixture sintetis atau
dokumen yang telah dipastikan tidak mengandung data pribadi.

---

# 72. LICENSE

Project harus memiliki file:

```text
LICENSE
```

License project ditentukan sebelum public release.

Pastikan license compatible dengan seluruh dependency dan code/reference yang
digunakan.

Jika menggunakan atau mengadaptasi code dari project lain, ikuti kewajiban
attribution sesuai license project tersebut.

---

# 73. CONTRIBUTING.md

Project public harus menyediakan panduan kontribusi.

Minimal mencakup:

```text
How to setup development environment
How to run tests
Coding standards
Pull request rules
Security considerations
```

Contributor tidak boleh mengirim:

```text
Real patient PDF
Medical record
Private hospital document
```

ke repository.

---

# 74. SECURITY.md

Repository harus memiliki `SECURITY.md`.

Tujuan:

- Menerima laporan vulnerability.
- Menerima laporan PDF security bypass.
- Menerima laporan sanitizer weakness.
- Menerima laporan dependency vulnerability.

Security report sebaiknya tidak dipublikasikan langsung sebagai GitHub issue
sebelum diperiksa.

Template minimal:

```text
# Security Policy

## Supported Versions

Only actively maintained versions are supported.

## Reporting a Vulnerability

If you discover a security vulnerability in PDF SafeTools,
please report it privately to the project maintainer.

Do not upload sensitive PDF files to public GitHub issues.

Do not upload patient data or medical records.

Include:

- Application version
- Windows version
- Description
- Reproduction steps
- Sanitizer rule involved
- Minimal safe sample if available

Never include real patient data.
```

---

# 75. CHANGELOG.md

Setiap release harus mencatat:

```text
Added
Changed
Fixed
Security
Known Issues
```

Contoh:

```text
## [1.1.0]

### Added
- PDF scanner
- External URI detection

### Security
- Improved JavaScript detection

### Fixed
- PDF merge issue
```

---

# 76. README.md

README minimal harus menjelaskan:

```text
Project
Features
Installation
Usage
Security
Privacy
Disclaimer
Development
License
```

README harus menyebutkan:

```text
Developed based on technical needs at:
RSUD Bantarangin Ponorogo
Ponorogo, Jawa Timur, Indonesia
```

dengan disclaimer bahwa project bukan aplikasi resmi institusi.

---

# 77. Definition of Done

Fitur dianggap selesai jika:

- UI bekerja.
- Input tervalidasi.
- Error ditangani.
- Output PDF valid.
- Temporary file dibersihkan.
- Test tersedia.
- Test berhasil.
- Tidak merusak fitur existing.
- Berjalan di Windows.
- Tidak membutuhkan internet.

Untuk sanitizer:

- Finding dapat dideteksi.
- Finding dapat dibersihkan.
- Output dapat dibuka.
- Output dapat diproses kembali.
- Output dapat di-scan kembali.
- Hasil scan sesuai konfigurasi.
- Tidak mengubah konten visual yang tidak perlu.

---

# 78. First AI Development Task

AI coding agent **jangan langsung membuat seluruh aplikasi**.

Task pertama:

```text
1. Baca PROJECT.md.
2. Buat struktur project.
3. Buat pyproject.toml.
4. Buat requirements.txt.
5. Buat requirements-dev.txt.
6. Setup PySide6.
7. Buat Main Window.
8. Buat Sidebar Navigation.
9. Buat Dashboard.
10. Buat Settings placeholder.
11. Buat About page.
12. Buat footer dengan informasi developer.
13. Tambahkan clickable GitHub Profile:
    https://github.com/yahya06
14. Tambahkan informasi Project Origin:
    RSUD Bantarangin Ponorogo
    Ponorogo, Jawa Timur, Indonesia
15. Jangan tampilkan Project Repository karena repository belum dibuat.
16. Buat logging dasar.
17. Pastikan aplikasi berjalan dengan:

    python -m app.main

18. Tambahkan basic test.
19. Jalankan test.
20. Jangan implementasikan PDF sanitizer pada task pertama.
```

Tahap berikutnya:

```text
Task 2
PDF validation + PDF information

Task 3
Merge PDF

Task 4
Split PDF

Task 5
Organize PDF

Task 6
Compress PDF

Task 7
PDF Scanner

Task 8
PDF Sanitizer

Task 9
JKN Safe Mode

Task 10
Batch Processing

Task 11
Packaging Windows

Task 12
Installer + Release
```

---

# 79. Final Product Goal

Target akhir:

```text
┌──────────────────────────────────────────────┐
│              PDF SafeTools                  │
│                                              │
│  PDF Tools                                   │
│                                              │
│  Merge       Split       Compress             │
│  Rotate      Reorder     PDF → Image          │
│  Image → PDF                                  │
│                                              │
│  PDF Security                                │
│                                              │
│  Scan PDF        Sanitize PDF                │
│                                              │
│  JKN Safe Mode                               │
│                                              │
│  🔒 Local Processing                         │
│  🔒 No Cloud                                 │
│  🔒 Privacy First                            │
│                                              │
└──────────────────────────────────────────────┘
```

Aplikasi akhir harus dapat dijalankan hanya dengan:

```text
Windows
+
PDFSafeTools.exe
```

Tanpa:

```text
Laravel
Apache
PHP
MySQL
Docker
WSL
Browser
Cloud
```

---

# 80. Project Principles

Seluruh pengembangan PDF SafeTools harus mengikuti prinsip:

```text
LOCAL FIRST
PRIVACY FIRST
SECURITY FIRST
SIMPLE BY DEFAULT
TEST EVERYTHING
NO UNNECESSARY DEPENDENCIES
NO PATIENT DATA IN REPOSITORY
NO CLOUD PROCESSING
NO FALSE SECURITY CLAIMS
```

Tujuan utama project bukan hanya membuat PDF utility,
tetapi membuat **tool desktop yang praktis, aman, transparan,
dan dapat diaudit secara teknis**.

---

# 81. Project Identity Summary

| Item | Value |
|---|---|
| Application | PDF SafeTools |
| Developer | Yahya |
| GitHub Profile | https://github.com/yahya06 |
| Repository | https://github.com/yahya06/pdf-safetools.git |
| Repository Status | Aktif |
| Project Origin | RSUD Bantarangin Ponorogo |
| Location | Ponorogo, Jawa Timur, Indonesia |
| Platform | Windows Desktop |
| Language | Python |
| GUI | PySide6 |
| PDF Library | pikepdf / PyMuPDF |
| Compression | Ghostscript |
| Processing | Local / Offline |
| Database | Tidak diperlukan |
| Web Server | Tidak diperlukan |
| Laravel | Tidak digunakan |
| Docker | Tidak digunakan untuk runtime |
| WSL | Tidak diperlukan untuk runtime |

---

# 82. Initial Repository Checklist

Sebelum membuat repository public:

```text
[ ] Review PROJECT.md
[ ] Tentukan LICENSE
[ ] Buat README.md
[ ] Buat SECURITY.md
[ ] Buat CONTRIBUTING.md
[ ] Buat CHANGELOG.md
[ ] Buat .gitignore
[ ] Pastikan tidak ada data pasien
[ ] Pastikan tidak ada credential
[ ] Pastikan tidak ada PDF asli rumah sakit
[ ] Pastikan tidak ada production log
[ ] Pastikan dependency license diperiksa
[ ] Pastikan attribution project referensi diperiksa
[ ] Jalankan test
[ ] Build Windows berhasil
[ ] Test executable pada PC Windows bersih
```

---

# 83. Release Checklist

Sebelum setiap release:

```text
[ ] Update version
[ ] Update CHANGELOG.md
[ ] Run unit tests
[ ] Run security tests
[ ] Run sanitizer regression tests
[ ] Build Windows executable
[ ] Test executable
[ ] Test installer
[ ] Test portable build jika tersedia
[ ] Check dependencies
[ ] Check licenses
[ ] Check GitHub release notes
[ ] Check no sensitive data included
```

---

# 84. Long-Term Roadmap

Future features yang dapat dipertimbangkan:

```text
[ ] OCR
[ ] PDF/A conversion
[ ] Digital signature inspection
[ ] Certificate inspection
[ ] Advanced metadata viewer
[ ] Batch processing
[ ] Watch folder
[ ] Portable mode
[ ] Windows installer
[ ] Automatic update
[ ] Accessibility improvements
[ ] Multi-language UI
```

Fitur berikut **tidak menjadi prioritas**:

```text
[ ] Cloud PDF processing
[ ] User account
[ ] SaaS backend
[ ] Online document storage
```

---

# 85. Final Development Rule

Jika terjadi konflik antara kenyamanan, fitur, dan keamanan dokumen, project
harus memprioritaskan:

```text
1. Data Privacy
2. Security
3. Data Integrity
4. Reliability
5. Usability
6. Performance
7. Additional Features
```

Jangan menambahkan fitur yang menyebabkan dokumen PDF harus keluar dari komputer
pengguna tanpa persetujuan eksplisit.

---

**End of PROJECT.md**
