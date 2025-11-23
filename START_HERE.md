# 🚀 Quick Start Guide

## Start the Backend Server

**IMPORTANT:** The backend must be running before the frontend can connect!

### Option 1: Use the Startup Script (Easiest)

```bash
cd /home/husain/hiring-assistant
./start_backend.sh
```

### Option 2: Manual Start

```bash
cd /home/husain/hiring-assistant/backend
source ../venv/bin/activate
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Verify Backend is Running

Open a **new terminal** and run:

```bash
curl http://localhost:8000/health
```

Should return: `{"status":"healthy"}`

If you see connection errors, the backend is not running.

## Start the Frontend

In a **separate terminal**:

```bash
cd /home/husain/hiring-assistant/frontend
npm run dev
```

The frontend will start at `http://localhost:3000`

## Test the Application

1. Open your browser: `http://localhost:3000`
2. The chat should automatically start
3. If you see "Failed to start chat", check:
   - Backend is running (test with `curl http://localhost:8000/health`)
   - No errors in the backend terminal
   - Browser console (F12) for detailed errors

## Troubleshooting

### "Failed to fetch" Error

This means the backend is not running or not accessible.

**Solution:**
1. Make sure the backend server is running (see above)
2. Check the backend terminal for any error messages
3. Verify: `curl http://localhost:8000/health` returns `{"status":"healthy"}`

### Backend Won't Start

**Check:**
1. Virtual environment is activated: `source ../venv/bin/activate`
2. Dependencies installed: `pip install -r requirements.txt`
3. OpenAI API key is set (check `.env` file)

### Routes Not Loading

If you see "ERROR: Could not import routes" in the backend logs:
- Check that all files are in the correct locations
- Verify imports work: `python -c "from routes import router"`

## Quick Test Commands

```bash
# Test backend health
curl http://localhost:8000/health

# Test start-chat endpoint
curl -X POST http://localhost:8000/api/start-chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": null}'

# Check if servers are running
ps aux | grep -E "(uvicorn|next)"
```

## Need Help?

See `TROUBLESHOOTING.md` for detailed troubleshooting steps.

