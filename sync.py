#!/usr/bin/env python3
"""Quick sync script - run to copy workspace changes to Desktop folder."""

import shutil
import os
from pathlib import Path

SOURCE = Path("/home/husain/hiring-assistant")
DEST = Path("/home/husain/Desktop/Hiring Assistant")

EXCLUDE_DIRS = {'.git', '__pycache__', 'venv', 'node_modules', '.next', '.venv'}
EXCLUDE_SUFFIXES = {'.pyc', '.pyo', '.pyd', '.db'}

print("🔄 Syncing workspace -> Desktop")
print(f"From: {SOURCE}")
print(f"To  : {DEST}\n")

copied_files = 0
for root, dirs, files in os.walk(SOURCE):
    dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
    rel_path = os.path.relpath(root, SOURCE)
    dest_dir = DEST / rel_path
    dest_dir.mkdir(parents=True, exist_ok=True)

    for file_name in files:
        if any(file_name.endswith(suffix) for suffix in EXCLUDE_SUFFIXES):
            continue
        src_file = Path(root) / file_name
        dst_file = dest_dir / file_name
        try:
            shutil.copy2(src_file, dst_file)
            copied_files += 1
        except Exception as exc:
            print(f"  ⚠️ Skipped {src_file}: {exc}")

print(f"\n✅ Sync complete. Files copied: {copied_files}")

