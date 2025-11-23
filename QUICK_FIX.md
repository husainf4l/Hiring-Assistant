# Quick Fix for "Failed to fetch" Error

## The Problem
The frontend cannot connect to the backend server. This usually means the backend is not running.

## Solution

### Step 1: Start the Backend Server

Open a terminal and run:

```bash
cd /home/husain/hiring-assistant/backend
source ../venv/bin/activate
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

You should see output like:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
Database initialized
✓ API routes loaded successfully
INFO:     Application startup complete.
```

### Step 2: Verify Backend is Running

In another terminal, test the backend:

```bash
curl http://localhost:8000/health
```

Should return: `{"status":"healthy"}`

### Step 3: Test the Chat Endpoint

```bash
curl -X POST http://localhost:8000/api/start-chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": null}'
```

Should return a JSON response with `session_id` and `response`.

### Step 4: Refresh Frontend

Go to `http://localhost:3000` and refresh the page. The chat should now start.

## If Still Not Working

1. **Check for errors in the backend terminal** - Look for import errors or other issues
2. **Check browser console (F12)** - Look for CORS errors or network errors
3. **Verify both servers are running:**
   - Backend: `http://localhost:8000`
   - Frontend: `http://localhost:3000`

## Common Issues

- **Port 8000 already in use**: Kill the existing process: `pkill -f uvicorn`
- **Import errors**: Make sure you're in the `backend` directory when starting
- **OpenAI API key missing**: Create `.env` file with `OPENAI_API_KEY=your_key`

