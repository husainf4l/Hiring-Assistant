# 🔄 Auto-Sync to Desktop

## Quick Sync After Editing

After you edit any file in this workspace, run:

```bash
./sync_to_desktop.sh
```

This will sync all changes to: `/home/husain/Desktop/Hiring Assistant`

## One-Line Sync Command

```bash
rsync -av --exclude='venv' --exclude='__pycache__' --exclude='*.pyc' --exclude='node_modules' --exclude='.next' /home/husain/hiring-assistant/ "/home/husain/Desktop/Hiring Assistant/"
```

## Better Solution: Work in Desktop Folder

Instead of syncing, **open the Desktop folder directly** in your editor:

```bash
cd "/home/husain/Desktop/Hiring Assistant"
```

Then all your edits will be saved directly to the Desktop location!

## Current Setup

- **Edit Location:** `/home/husain/hiring-assistant` (current workspace)
- **Save Location:** `/home/husain/Desktop/Hiring Assistant` (Desktop folder)

