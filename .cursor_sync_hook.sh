#!/bin/bash
# This script can be run automatically after file saves
# Syncs changes to Desktop folder

DEST="/home/husain/Desktop/Hiring Assistant"
SOURCE="/home/husain/hiring-assistant"

# Quick sync (only changed files)
rsync -av \
  --exclude='venv' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  --exclude='node_modules' \
  --exclude='.next' \
  --exclude='.git' \
  --exclude='*.db' \
  "$SOURCE/" "$DEST/" > /dev/null 2>&1

