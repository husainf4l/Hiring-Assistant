#!/usr/bin/env python3
"""Quick sync script - Run this after editing files to sync to Desktop"""

import shutil
import os
from pathlib import Path

source = Path("/home/husain/hiring-assistant")
dest = Path("/home/husain/Desktop/Hiring Assistant")

exclude_dirs = {'.git', '__pycache__', 'venv', 'node_modules', '.next', '.venv'}
exclude_files = {'.pyc', '.pyo', '.pyd', '.db'}

print("🔄 Syncing to Desktop folder...")
print(f"From: {source}")
print(f"To: {dest}\n")

copied = 0
for root, dirs, files in os.walk(source):
    dirs[:] = [d for d in dirs if d not in exclude_dirs]
    rel = os.path.relpath(root, source)
    dst_dir = dest / rel
    dst_dir.mkdir(parents=True, exist_ok=True)
    
    for f in files:
        if any(f.endswith(e) for e in exclude_files):
            continue
        try:
            shutil.copy2(source / rel / f, dst_dir / f)
            copied += 1
        except: pass

print(f"✅ Synced {copied} files to: {dest}")

