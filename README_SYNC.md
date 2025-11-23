# 🔄 Sync to Desktop

## Quick Sync Command

After editing files here, sync to Desktop:

```bash
./sync_to_desktop.sh
```

Or manually:

```bash
rsync -av --exclude='venv' --exclude='__pycache__' --exclude='*.pyc' --exclude='node_modules' --exclude='.next' /home/husain/hiring-assistant/ "/home/husain/Desktop/Hiring Assistant/"
```

## Desktop Location

All changes should be synced to:
`/home/husain/Desktop/Hiring Assistant`

## Recommendation

**Work directly in the Desktop folder** to avoid sync issues:
```bash
cd "/home/husain/Desktop/Hiring Assistant"
```

