#!/bin/bash
# Auto-sync script - Run this after making edits in the workspace
# This syncs all changes to /home/husain/Desktop/Hiring Assistant

SOURCE="/home/husain/hiring-assistant"
DEST="/home/husain/Desktop/Hiring Assistant"

echo "🔄 Syncing to Desktop folder..."
echo ""

rsync -av \
  --exclude='venv' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  --exclude='node_modules' \
  --exclude='.next' \
  --exclude='.git' \
  --exclude='*.db' \
  --delete \
  "$SOURCE/" "$DEST/"

echo "✅ Synced to: $DEST"

