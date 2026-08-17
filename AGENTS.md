# AGENTS.md

## What is this

Windows desktop app for local PDF merge/split/compress/scan/sanitize. Python 3.12+ / PySide6. No server, no cloud, no browser, no Docker.

`PROJECT.md` is the authoritative spec. Read the relevant sections before any task.

Repo: https://github.com/yahya06/pdf-safetools.git

## Current state (Phase 1 done)

GUI shell only: Dashboard, Settings placeholder, About. No PDF processing yet.

Installed runtime dep is **PySide6 only**. pikepdf / PyMuPDF / Ghostscript are specified for later phases — do not add them until that phase.

Do not implement the sanitizer, scanner, or other PDF tools until their phase. Phase order in `PROJECT.md` §65 / §78.

## Hard rules

- Never upload or send PDFs externally. All processing is local.
- Never overwrite original files. Output suffixes: `_clean`, `_compressed`. Merge output: `merged.pdf`.
- Never `os.system()` or `subprocess.run(..., shell=True)` with user data. Argument lists only.
- Never log PDF content, patient data, or passwords.
- Never execute JavaScript or PDF actions. Scanner is static analysis only.
- Never add Laravel / PHP / React / Electron / Docker / WSL / browser deps. Stack is Python + PySide6 + pikepdf + PyMuPDF + Ghostscript.
- Never commit patient data, real hospital documents, credentials, or production logs.

## Sanitizer (when you reach that phase)

- Do **not** search-and-delete `http://` / `https://` / `www.` — printed text URLs are not dangerous.
- Target PDF objects/actions: `/URI`, `/Launch`, `/GoToR`, `/GoToE`, `/SubmitForm`, `/ImportData`, `/EmbeddedFiles`, `/RichMedia`, `/Movie`, `/Sound`, `/3D`.
- Required flow: Scan → Sanitize → Save → Re-scan → Report.
- Severity: `INFO` `LOW` `MEDIUM` `HIGH` `CRITICAL`. Risk: `SAFE` `LOW` `MEDIUM` `HIGH` `CRITICAL`.
- `SAFE` is an app status only. Never claim "free of malware". Say "No configured findings detected".

Treat every PDF as sensitive health data by default.

## Commands

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt        # runtime
pip install -r requirements-dev.txt    # includes runtime + ruff/mypy/pytest
python -m app.main                     # run app
ruff check .
ruff format .
mypy app/
pytest
```

Verify in that order. `pyproject.toml` sets `tool.pytest.ini_options.pythonpath = ["."]` — without it, pytest cannot import `app`.

Ruff: line-length 100, rules E/F/I. Mypy: `strict = true`.

## Layout that exists

```
app/main.py              entrypoint
app/ui/                  MainWindow + sidebar (QListWidget + QStackedWidget)
                         pages: dashboard, settings_page, about_page
app/config/settings.py   APP_INFO + APP_DATA_DIR / LOG_DIR / TEMP_DIR
app/utils/logging_utils.py   rotating log to %LOCALAPPDATA%\PDFSafeTools\logs
tests/test_foundation.py
```

Planned later (do not create empty stubs): `app/services/`, `app/security/`, `app/models/`, `app/workers/`, `sample_pdfs/`, `scripts/`.

## Conventions agents miss

- Developer/origin strings live only in `APP_INFO` (`app/config/settings.py`). Do not scatter them.
- `APP_INFO["repository"]` is still `None` in code. Hide any Project Repository button while it is `None`. `tests/test_foundation.py` asserts this. PROJECT.md already lists the GitHub URL — update `APP_INFO` and that test together, not one without the other.
- App data: `%LOCALAPPDATA%\PDFSafeTools\` (logs, temp, output, config, cache). Never `C:\Program Files\`.
- PDF validation (when added): extension + `%PDF-` signature + pikepdf parse. Not extension alone.
- Long work goes on QThread/QRunnable. No fake progress bars.
- Logging levels: INFO / WARNING / ERROR only.
- Sample PDFs (when added) go under `sample_pdfs/<threat>/`. Synthetic fixtures only — no real hospital files, no live malware.
- Every security bug becomes a regression test with a fixture.
