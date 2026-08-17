# AGENTS.md

## What is this

Windows desktop app for PDF merge/split/compress/scan/sanitize. Python 3.12+ / PySide6 / pikepdf / PyMuPDF / Ghostscript. No server, no cloud, no browser, no Docker.

## Read before working

`PROJECT.md` is the authoritative spec (~2500 lines). Every architectural decision, security rule, and feature scope is there. Read the relevant sections before any task.

## Hard rules — do not violate

- **Never upload or send PDFs externally.** All processing is local. No cloud, no API calls, no AI services.
- **Never overwrite original files.** Output goes to `_clean`, `_compressed`, etc.
- **Never use `os.system()` or `subprocess.run(..., shell=True)` with user data.** Always use argument lists.
- **Never log PDF content, patient data, or passwords.**
- **Never run JavaScript or PDF actions during scanning.** Scanner is static analysis only.
- **Never add Laravel/PHP/React/Electron/Docker/WSL/browser dependencies.** Tech stack is fixed: Python + PySide6 + pikepdf + PyMuPDF + Ghostscript.
- **Never commit patient data, real hospital documents, credentials, or production logs.**

## Sanitizer gotchas

- Do NOT just search for `http://` / `https://` / `www.` and delete them. Text URLs on a page are not dangerous.
- Sanitizer must target PDF objects/actions: `/URI`, `/Launch`, `/GoToR`, `/GoToE`, `/SubmitForm`, `/ImportData`, `/EmbeddedFiles`, `/RichMedia`, `/Movie`, `/Sound`, `/3D`.
- Every sanitization must be followed by re-scan: Scan → Sanitize → Save → Re-scan → Report.
- Severity levels: `INFO`, `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`. Risk levels: `SAFE`, `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`.
- "SAFE" is an application status only — never claim it means "free of malware". Use "No configured findings detected" instead.

## Security context

PDFs may contain health/medical data. Treat every PDF as sensitive data by default.

## Commands

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt        # runtime deps
pip install -r requirements-dev.txt    # dev/test deps
python -m app.main                     # run app
pytest                                 # tests
ruff check .                           # lint
ruff format .                          # format
mypy app/                              # type check
```

## Project structure (key boundaries)

```
app/main.py          — entrypoint (python -m app.main)
app/ui/              — PySide6 GUI (main_window, sidebar nav, pages)
app/services/        — business logic (merge, split, compress, organize, render, scanner, sanitizer)
app/security/        — scanner + sanitizer engine (scanner.py, sanitizer.py, rules.py, findings.py)
app/models/          — data models (scan_result, sanitize_result, pdf_info)
app/workers/         — QThread/QRunnable workers for non-blocking ops
app/utils/           — file, hash, logging, system utilities
app/config/settings.py — centralized config + APP_INFO dict
sample_pdfs/         — test fixtures by threat type (safe, javascript, external_uri, open_action, etc.)
tests/               — pytest + pytest-qt
scripts/             — build.py, package.py (PyInstaller packaging)
```

## Conventions

- PDF validation: check extension + `%PDF-` signature + pikepdf parse, not just extension.
- Output naming: `original_clean.pdf`, `original_compressed.pdf`, `merged.pdf`.
- Temp files: `%LOCALAPPDATA%\PDFSafeTools\temp` — clean after use.
- App data: `%LOCALAPPDATA%\PDFSafeTools\` (logs, temp, output, config, cache). Never in `C:\Program Files\`.
- UI: sidebar navigation, Qt stylesheet themes (Light/Dark/System).
- Logging: rotating log, levels INFO/WARNING/ERROR only. No PDF content in logs.
- Thread long operations (QThread/QRunnable). Never freeze UI. Show real progress only.
- Developer info centralized in `APP_INFO` dict in `app/config/settings.py`. Do not scatter across files.
- `repository` field in APP_INFO is currently `None` — UI must hide the Project Repository button when `None`.

## Testing

- Framework: pytest + pytest-qt.
- Test fixtures: `sample_pdfs/` directories by threat category (safe, javascript, external_uri, open_action, launch, embedded, annotation, multimedia, encrypted, malformed).
- Every security bug must become a regression test with a fixture.
- Test files: `tests/test_merge.py`, `test_split.py`, `test_compress.py`, `test_scanner.py`, `test_sanitizer.py`.
