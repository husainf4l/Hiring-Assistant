# 🔄 How to Restart the Backend Server

## The Problem
If you're getting a **404 error** on `/api/start-chat`, the routes aren't being loaded. This usually means:
1. The server needs to be restarted to pick up code changes
2. There's an import error preventing routes from loading

## Solution: Restart the Server

### Step 1: Stop the Current Server
In the terminal where the server is running, press **Ctrl+C** to stop it.

### Step 2: Start the Server Again

```bash
cd /home/husain/hiring-assistant/backend
source ../venv/bin/activate
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Step 3: Check for Success Messages

Look for these messages in the server output:
```
Database initialized
✓ API routes loaded successfully
✓ Registered X API routes
INFO:     Application startup complete.
```

### Step 4: Check for Errors

If you see:
- `ERROR: Could not import routes` → There's an import problem
- `ERROR: Failed to initialize orchestrator` → There's an initialization problem
- No "✓ API routes loaded successfully" message → Routes didn't load

### Step 5: Verify Routes are Loaded

Open a new terminal and test:

```bash
# Check health
curl http://localhost:8000/health

# List all routes (debug endpoint)
curl http://localhost:8000/debug/routes

# Test the start-chat endpoint
curl -X POST http://localhost:8000/api/start-chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": null}'
```

## Quick Test Script

You can also test if routes load correctly:

```bash
cd /home/husain/hiring-assistant/backend
../venv/bin/python test_routes.py
```

This will show you if routes can be imported and registered.

## Common Issues

### Issue: "ERROR: Could not import routes"
**Solution:** Check that all dependencies are installed:
```bash
cd backend
source ../venv/bin/activate
pip install -r requirements.txt
```

### Issue: "ERROR: Failed to initialize orchestrator"
**Solution:** Check that OpenAI API key is set:
```bash
# Check .env file exists
cat backend/.env | grep OPENAI_API_KEY
```

### Issue: Routes load but still get 404
**Solution:** Make sure you're using the correct URL:
- Frontend should call: `http://localhost:8000/api/start-chat`
- Backend route is: `/api/start-chat` (with prefix)

## After Restarting

1. Refresh your browser at `http://localhost:3000`
2. The chat should now start successfully
3. Check browser console (F12) for any remaining errors

