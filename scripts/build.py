#!/usr/bin/env python3
"""
Build script for PDF SafeTools using PyInstaller.

Usage:
    python scripts/build.py [--clean] [--onefile]
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Build PDF SafeTools executable")
    parser.add_argument(
        "--clean", action="store_true", help="Remove build artifacts before building"
    )
    parser.add_argument("--onefile", action="store_true", help="Build single-file executable")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent
    spec_file = project_root / "pdfsafetools.spec"

    if args.clean:
        for path in (project_root / "build", project_root / "dist", project_root / "__pycache__"):
            if path.exists():
                shutil.rmtree(path, ignore_errors=True)

    # Ensure spec exists
    if not spec_file.exists():
        generate_spec(project_root, spec_file)

    cmd = ["pyinstaller", "--noconfirm"]
    if args.onefile:
        cmd.append("--onefile")
    cmd.append(str(spec_file))

    result = subprocess.run(cmd, cwd=project_root)
    return result.returncode


def generate_spec(project_root: Path, spec_file: Path) -> None:
    """Generate a PyInstaller spec file tailored for this project."""
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

project_root = Path(r"{project_root.as_posix()}")

block_cipher = None

a = Analysis(
    [str(project_root / "app" / "main.py")],
    pathex=[str(project_root)],
    binaries=[],
    datas=[
        (str(project_root / "app" / "assets" / "images" / "logo.png"), "app/assets/images"),
    ],
    hiddenimports=[
        "pikepdf",
        "fitz",
        "PySide6.QtCore",
        "PySide6.QtGui",
        "PySide6.QtWidgets",
        "PySide6.QtPrintSupport",
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[
        "tkinter",
        "matplotlib",
        "numpy",
        "scipy",
        "pandas",
        "jupyter",
        "notebook",
        "IPython",
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="PDFSafeTools",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(project_root / "app" / "assets" / "images" / "logo.png"),
    version_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="PDFSafeTools",
)
'''
    spec_file.write_text(spec_content)


if __name__ == "__main__":
    sys.exit(main())
