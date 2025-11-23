# Troubleshooting Guide

## "Failed to start chat" Error

If you're seeing "Failed to start chat. Please try again." error in the frontend, follow these steps:

### Step 1: Verify Backend is Running

```bash
curl http://localhost:8000/health
```

Should return: `{"status":"healthy"}`

### Step 2: Test the API Endpoint Directly

```bash
curl -X POST http://localhost:8000/api/start-chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": null}'
```

If this returns `{"detail":"Not Found"}`, the routes are not loading.

### Step 3: Check Server Logs

Look at the terminal where uvicorn is running. You should see:
- `✓ API routes loaded successfully` - Routes loaded
- `ERROR: Could not import routes: ...` - Import error
- `ERROR: Failed to initialize orchestrator: ...` - Orchestrator error

### Step 4: Restart the Backend Server

1. Stop the current server (Ctrl+C or kill the process)
2. Navigate to backend:
   ```bash
   cd /home/husain/hiring-assistant/backend
   ```
3. Activate virtual environment:
   ```bash
   source ../venv/bin/activate
   ```
4. Start server:
   ```bash
   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Step 5: Check for Import Errors

If you see import errors in the logs, the issue is likely:
- Missing dependencies (run `pip install -r requirements.txt`)
- Relative import issues (should be fixed in the code)
- Missing OpenAI API key

### Step 6: Verify OpenAI API Key

```bash
cd backend
source ../venv/bin/activate
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('OPENAI_API_KEY:', 'SET' if os.getenv('OPENAI_API_KEY') else 'NOT SET')"
```

If NOT SET, create a `.env` file:
```bash
cd backend
cp env.example .env
# Then edit .env and add your OPENAI_API_KEY
```

### Step 7: Check Browser Console

Open browser DevTools (F12) and check:
- Network tab: See if the request to `/api/start-chat` is failing
- Console tab: Look for JavaScript errors
- Check the actual error message from the API

### Common Issues and Solutions

1. **404 Not Found on /api/start-chat**
   - Routes not loading - check server startup logs
   - Restart the server
   - Check that `routes.py` imports successfully

2. **500 Internal Server Error**
   - Check server logs for the actual error
   - Usually an OpenAI API issue or database issue
   - Verify OPENAI_API_KEY is set

3. **CORS Error**
   - Backend CORS is configured for `http://localhost:3000`
   - Make sure frontend is running on port 3000
   - Check browser console for CORS errors

4. **Database Errors**
   - Database is auto-created on first run
   - Check file permissions in backend directory
   - SQLite database file: `hiring_assistant.db`

### Quick Fix Script

Run this to check everything:

```bash
cd /home/husain/hiring-assistant/backend
source ../venv/bin/activate

# Check dependencies
pip install -r requirements.txt

# Check imports
python -c "from routes import router; print('Routes OK')"

# Check OpenAI key
python -c "import os; from dotenv import load_dotenv; load_dotenv(); assert os.getenv('OPENAI_API_KEY'), 'OPENAI_API_KEY not set'"

# Start server
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

