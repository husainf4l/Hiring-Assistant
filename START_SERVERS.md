# How to Start the Servers

## Backend (FastAPI)

1. Navigate to backend directory:
```bash
cd /home/husain/hiring-assistant/backend
```

2. Activate virtual environment:
```bash
source ../venv/bin/activate
```

3. Start the server:
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The server will start on `http://localhost:8000`

## Frontend (Next.js)

1. Navigate to frontend directory:
```bash
cd /home/husain/hiring-assistant/frontend
```

2. Install dependencies (if not already done):
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will start on `http://localhost:3000`

## Troubleshooting

If you see "Failed to start chat" error:

1. **Check backend is running:**
   ```bash
   curl http://localhost:8000/health
   ```
   Should return: `{"status":"healthy"}`

2. **Test the start-chat endpoint:**
   ```bash
   curl -X POST http://localhost:8000/api/start-chat \
     -H "Content-Type: application/json" \
     -d '{"user_id": null}'
   ```

3. **Check server logs** for import errors or other issues

4. **Verify OpenAI API key is set:**
   ```bash
   cd backend
   source ../venv/bin/activate
   python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('OPENAI_API_KEY:', 'SET' if os.getenv('OPENAI_API_KEY') else 'NOT SET')"
   ```

5. **Check if routes are loaded:**
   Visit `http://localhost:8000/docs` and see if `/api/start-chat` endpoint is listed

## Common Issues

- **404 Not Found on /api/start-chat**: Routes not loading - check server startup logs
- **Import errors**: Make sure you're running from the backend directory
- **Database errors**: Database will be auto-created on first run
- **OpenAI errors**: Make sure OPENAI_API_KEY is set in .env file

