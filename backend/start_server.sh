#!/bin/bash
# Start script for FastAPI server

cd "$(dirname "$0")"
source ../venv/bin/activate

echo "Starting FastAPI server..."
echo "Checking imports..."

python -c "
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath('.')))

try:
    from routes import router
    print('✓ Routes imported successfully')
    print(f'✓ Found {len(router.routes)} routes')
except Exception as e:
    print(f'✗ Routes import failed: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
"

if [ $? -eq 0 ]; then
    echo "Starting uvicorn..."
    python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
else
    echo "Failed to import routes. Please check the errors above."
    exit 1
fi


