# AGENTS.md

## Project

Windows desktop PDF utility/security app. Python 3.12+, PySide6, pikepdf, PyMuPDF, optional Ghostscript. Processing is local; no server, cloud, browser, Docker, Laravel, PHP, React, or Electron.

Read relevant `PROJECT.md` sections before changing architecture or phase scope.

Repository: https://github.com/yahya06/pdf-safetools.git

## Current phase

Phases 1–3 are implemented: GUI foundation, PDF core, and Ghostscript compression. Scanner and sanitizer are not implemented; do not create them until their planned phases.

Ghostscript is not installed on the current development machine. Compression tests cover command construction and missing-executable handling, not real compression.

## Commands

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -r requirements-dev.txt
python -m app.main
ruff check .
ruff format .
mypy app/
pytest
pytest tests/test_pdf_core.py
pytest tests/test_compress.py
```

Run verification in this order: `ruff check .`, `ruff format .`, `mypy app/`, `pytest`. The pytest root import works because `pyproject.toml` sets `pythonpath = ["."]`. Mypy is strict and ignores missing third-party stubs.

## Entry points and boundaries

- `app/main.py`: application entry point (`python -m app.main`).
- `app/ui/`: PySide6 pages and sidebar wiring in `main_window.py`.
- `app/services/pdf_service.py`: PDF validation, metadata, merge, split, page transform.
- `app/services/render_service.py`: PDF/image conversion.
- `app/services/compress_service.py`: Ghostscript discovery, safe argument-list command, presets, size comparison.
- `app/config/settings.py`: centralized `APP_INFO` and `%LOCALAPPDATA%\PDFSafeTools` paths.
- `tests/`: pytest tests; current suites are `test_foundation.py`, `test_pdf_core.py`, and `test_compress.py`.

## Non-obvious constraints

- PDF validation requires `.pdf`, `%PDF-` signature, and successful pikepdf parsing.
- Never overwrite originals. Use `_clean`, `_compressed`, or `merged.pdf` output names; `_ensure_new_output` rejects existing outputs.
- External processes must use argument lists, never `shell=True` or `os.system()`. Ghostscript commands must retain `-dSAFER`.
- Do not log PDF content, patient data, passwords, image content, or sensitive filenames.
- Treat every PDF as sensitive health data. Never commit real PDFs, patient data, credentials, logs, or active malware fixtures.
- Long PDF operations must not freeze the Qt UI; use QThread/QRunnable when adding expensive work. Do not fake progress.
- Runtime application data belongs under `%LOCALAPPDATA%\PDFSafeTools\`, never `C:\Program Files\`.
- Developer/project identity belongs in `APP_INFO`; do not duplicate it across UI files. `APP_INFO["repository"]` remains `None`, so repository UI must stay hidden until configured.

## Future security phases

Scanner must be static analysis only: never execute JavaScript, PDF actions, embedded executables, launches, or external URLs. Sanitizer targets PDF objects/actions, not printed `http://`, `https://`, or `www.` text. Sanitization flow is Scan → Sanitize → Save → Re-scan → Report. Never describe `SAFE` as malware-free; use `No configured findings detected`.

Every security bug requires a synthetic fixture and regression test.

## Scope discipline

Do not add empty future directories or dependencies. Add pikepdf/PyMuPDF only for PDF-core work and Ghostscript integration only for compression. Keep outputs local and deterministic.
