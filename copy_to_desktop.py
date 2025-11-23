#!/usr/bin/env python3
"""Script to copy the Hiring Assistant project to Desktop"""

import shutil
import os
from pathlib import Path

# Source and destination paths
source = Path("/home/husain/hiring-assistant")
dest = Path.home() / "Desktop" / "Hiring Assistant"

# Exclude patterns
exclude_dirs = {'.git', '__pycache__', 'venv', 'node_modules', '.next', '.venv'}
exclude_files = {'.pyc', '.pyo', '.pyd', '.db'}

print(f"Copying from: {source}")
print(f"Copying to: {dest}")

# Create destination directory
dest.mkdir(parents=True, exist_ok=True)

# Copy files and directories
copied_files = 0
copied_dirs = 0

for root, dirs, files in os.walk(source):
    # Skip excluded directories
    dirs[:] = [d for d in dirs if d not in exclude_dirs]
    
    # Calculate relative path
    rel_path = os.path.relpath(root, source)
    dest_dir = dest / rel_path
    
    # Create destination directory
    if rel_path != '.':
        dest_dir.mkdir(parents=True, exist_ok=True)
        copied_dirs += 1
    
    # Copy files
    for file in files:
        # Skip excluded file types
        if any(file.endswith(ext) for ext in exclude_files):
            continue
        
        src_file = Path(root) / file
        dst_file = dest_dir / file
        
        try:
            shutil.copy2(src_file, dst_file)
            copied_files += 1
            if copied_files % 50 == 0:
                print(f"  Copied {copied_files} files...")
        except Exception as e:
            print(f"  Warning: Could not copy {src_file}: {e}")

print(f"\n✓ Copy completed!")
print(f"  - Files copied: {copied_files}")
print(f"  - Directories created: {copied_dirs}")
print(f"  - Destination: {dest}")

