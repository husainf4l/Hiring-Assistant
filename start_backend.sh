#!/bin/bash
# Simple script to start the FastAPI backend server

cd "$(dirname "$0")/backend"
source ../venv/bin/activate

echo "Starting FastAPI backend server..."
echo "Server will be available at: http://localhost:8000"
echo "API docs will be available at: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

