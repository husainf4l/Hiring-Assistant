# 🔄 Sync Instructions

## After Editing Files

When you edit files in this workspace (`/home/husain/hiring-assistant`), sync them to Desktop:

### Quick Sync (Python)
```bash
python3 sync.py
```

### Quick Sync (Bash)
```bash
./sync_to_desktop.sh
```

### Manual Sync
```bash
rsync -av --exclude='venv' --exclude='__pycache__' --exclude='*.pyc' --exclude='node_modules' --exclude='.next' /home/husain/hiring-assistant/ "/home/husain/Desktop/Hiring Assistant/"
```

## Desktop Location

All changes sync to:
**`/home/husain/Desktop/Hiring Assistant`**

## Best Practice

**Work directly in the Desktop folder** to avoid syncing:

```bash
cd "/home/husain/Desktop/Hiring Assistant"
# Open this folder in your editor
```

This way, all edits are saved directly to the Desktop location!

