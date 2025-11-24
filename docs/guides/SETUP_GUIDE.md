# 🚀 Setup Guide

Complete step-by-step instructions to get the HR Hiring Assistant running locally.

---

## 📋 Prerequisites

Before starting, ensure you have:

- **Python 3.8 or higher** - [Download](https://www.python.org/downloads/)
  ```bash
  python --version  # Should be 3.8+
  ```

- **Node.js 16+ with npm** - [Download](https://nodejs.org/)
  ```bash
  node --version   # Should be 16+
  npm --version    # Should be 8+
  ```

- **Git** - [Download](https://git-scm.com/)
  ```bash
  git --version
  ```

- **OpenAI API Key** - [Get one here](https://platform.openai.com/api-keys)

- **Text Editor** - VS Code recommended - [Download](https://code.visualstudio.com/)

---

## 🏗️ Installation Steps

### Step 1: Clone or Download the Repository

```bash
# Clone from GitHub
git clone https://github.com/husainf4l/Hiring-Assistant.git
cd Hiring-Assistant

# Or navigate to existing project
cd /path/to/hiring-assistant
```

### Step 2: Backend Setup

#### 2.1 Create Python Virtual Environment

```bash
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

✅ You should see `(venv)` prefix in your terminal

#### 2.2 Install Python Dependencies

```bash
# Install required packages
pip install -r requirements.txt
```

**What gets installed**:
- FastAPI - Web framework
- Uvicorn - ASGI server
- SQLAlchemy - Database ORM
- Pydantic - Data validation
- OpenAI - AI API client
- Python-dotenv - Environment variables

#### 2.3 Environment Configuration

```bash
# Copy example environment file
cp env.example .env

# Open and edit .env file
# macOS/Linux:
nano .env

# On Windows:
# Open .env in VS Code or Notepad
```

**Edit `.env` and add your OpenAI API key**:

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-your-actual-api-key-here

# Database URL
DATABASE_URL=sqlite:///./hiring_assistant.db

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Development
DEBUG=True
```

⚠️ **Never commit `.env` file to git** - It's already in `.gitignore`

#### 2.4 Initialize Database

```bash
# While still in backend directory with venv activated
python init_db.py
```

Expected output:
```
Database initialized successfully!
Created tables: chat_sessions, job_posts
```

✅ Database file created: `backend/hiring_assistant.db`

#### 2.5 Test Backend Setup

```bash
# Verify imports work
python test_imports.py

# You should see:
# ✅ All imports successful
```

### Step 3: Frontend Setup

#### 3.1 Navigate to Frontend Folder

```bash
# From root directory (leave backend/venv activated)
cd frontend
```

#### 3.2 Install Node Dependencies

```bash
# Install npm packages
npm install
```

**What gets installed**:
- Next.js - React framework
- TypeScript - Type safety
- React - UI library
- And many other dependencies

Expected output:
```
added XXX packages in X.XXs
```

#### 3.3 Verify Frontend Setup

```bash
# List installed packages
npm list | head -20

# Should show:
# frontend@1.0.0
# ├── next@...
# ├── react@...
# └── ...
```

### Step 4: Backend Initialization Script (Optional)

If `init_db.py` didn't work:

```bash
# From backend directory with venv activated
python init_db.py
```

Or manual initialization:
```bash
python -c "from database import init_db; init_db()"
```

---

## 🎯 Running the Application

### Terminal 1: Start Backend Server

```bash
# Navigate to project root
cd /path/to/hiring-assistant

# Activate Python environment
cd backend
source venv/bin/activate  # macOS/Linux
# or: venv\Scripts\activate  # Windows

# Start backend server
cd ..
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

✅ Backend ready: `http://localhost:8000`

**In a new terminal window:**

### Terminal 2: Start Frontend Server

```bash
# Navigate to frontend directory
cd /path/to/hiring-assistant/frontend

# Start development server
npm run dev
```

Expected output:
```
▲ Next.js 14.0.0
- Local:        http://localhost:3000
- Environments: .env.local

Ready in 0.0s
```

✅ Frontend ready: `http://localhost:3000`

---

## ✅ Verify Everything is Working

### Check Backend Health

```bash
# In a new terminal
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy", "message": "API is running"}
```

### Check Frontend

Open browser and visit: **http://localhost:3000**

You should see:
- HR Hiring Assistant header
- Chat panel on the left
- Preview panel on the right (empty)
- "Start Creating Post" button

### Test Full Flow

1. Click "Start Creating Post"
2. You should see first AI question
3. Type a response
4. See live preview update
5. Continue conversation
6. Save the post
7. Check dashboard

✅ Everything working!

---

## 🔧 Environment Configuration

### Backend Environment Variables

Create `backend/.env` with these variables:

```env
# Required: OpenAI API Configuration
OPENAI_API_KEY=sk-...your-key-here...

# Optional: Database
DATABASE_URL=sqlite:///./hiring_assistant.db

# Optional: Server Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Optional: Development Settings
DEBUG=True
LOG_LEVEL=INFO
```

### Frontend Environment Variables

Create `frontend/.env.local`:

```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000/api

# Optional: Environment
NEXT_PUBLIC_ENV=development
```

### API Endpoints Configuration

The frontend automatically connects to backend at:
```
http://localhost:8000/api
```

To change, edit `frontend/lib/api.ts`:
```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';
```

---

## 📁 Verify Project Structure

After setup, your project should look like:

```
hiring-assistant/
├── backend/
│   ├── venv/                    # Virtual environment
│   ├── agents/
│   │   ├── interview_agent.py
│   │   ├── composer_agent.py
│   │   └── formatter_agent.py
│   ├── main.py
│   ├── routes.py
│   ├── database.py
│   ├── .env                     # With your API key
│   └── hiring_assistant.db      # Database file
│
├── frontend/
│   ├── node_modules/            # Installed packages
│   ├── app/
│   │   ├── page.tsx
│   │   └── globals.css
│   ├── components/
│   │   ├── ChatPanel.tsx
│   │   └── PreviewPanel.tsx
│   ├── package.json
│   └── .env.local               # If needed
│
└── docs/                        # Documentation
    ├── ARCHITECTURE.md
    ├── API_DOCUMENTATION.md
    └── ...
```

---

## 🆘 Common Setup Issues

### Issue 1: Python Not Found

```bash
# Error: python: command not found
```

**Solution**:
```bash
# Check Python installation
python3 --version

# If using Python 3, use python3 instead:
python3 -m venv venv
```

### Issue 2: Virtual Environment Not Activating

```bash
# Error: venv is not recognized
```

**Solution**:
```bash
# Make sure you're in backend directory
cd backend

# On Windows, use:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Issue 3: OpenAI API Key Error

```bash
# Error: OpenAI API key not found
```

**Solution**:
1. Verify `.env` file exists in `backend/` folder
2. Check that `OPENAI_API_KEY=sk-...` is there
3. Restart backend server after adding key

### Issue 4: Port Already in Use

```bash
# Error: Address already in use (port 8000)
```

**Solution**:
```bash
# Find process using port 8000
# macOS/Linux:
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use different port:
python -m uvicorn backend.main:app --port 8001
```

### Issue 5: npm install Fails

```bash
# Error: npm ERR! code ERESOLVE
```

**Solution**:
```bash
# Clear npm cache and retry
npm cache clean --force
npm install

# Or use legacy peer deps:
npm install --legacy-peer-deps
```

### Issue 6: TypeScript Errors

```bash
# Error: Cannot find module types
```

**Solution**:
```bash
# Reinstall node_modules
rm -rf frontend/node_modules
npm install

# Regenerate next files:
npm run build
```

---

## 🔄 Starting Fresh

If you need to reset everything:

### Clear Backend

```bash
# Remove virtual environment
rm -rf backend/venv

# Remove database
rm backend/hiring_assistant.db

# Remove cache
rm -rf backend/__pycache__

# Then redo steps 2.1-2.4
```

### Clear Frontend

```bash
# Remove dependencies
rm -rf frontend/node_modules
rm frontend/package-lock.json

# Then redo step 3.2
```

---

## ✨ Additional Setup Options

### Using Docker (Optional)

If you have Docker installed:

```bash
# Build and run backend
docker build -t hiring-assistant-backend backend/
docker run -p 8000:8000 hiring-assistant-backend

# Build and run frontend
docker build -t hiring-assistant-frontend frontend/
docker run -p 3000:3000 hiring-assistant-frontend
```

### Using Scripts

We provide convenience scripts:

```bash
# Start backend
./scripts/start_backend.sh

# Start frontend (create if needed)
cd frontend && npm run dev
```

### Development Tools Setup

**Install development dependencies**:

```bash
# Backend development tools
pip install pytest pytest-cov black flake8

# Frontend development tools
npm install --save-dev prettier eslint
```

---

## 📚 Next Steps

After successful setup:

1. **📖 Read Documentation**
   - [ARCHITECTURE.md](./ARCHITECTURE.md) - Understand the system
   - [API_DOCUMENTATION.md](./API_DOCUMENTATION.md) - Learn the API

2. **🧪 Test the Application**
   - Try creating a job post
   - Test all features
   - Check the dashboard

3. **🔧 Explore the Code**
   - Review `backend/main.py` - Entry point
   - Check `frontend/app/page.tsx` - Main UI
   - Examine `backend/agents/` - AI logic

4. **🚀 Deploy** (When ready)
   - See [DEPLOYMENT.md](./guides/DEPLOYMENT.md)
   - Set up production environment
   - Configure database

5. **📝 Contribute** (Optional)
   - See [CONTRIBUTING.md](./guides/CONTRIBUTING.md)
   - Make improvements
   - Share changes

---

## 🆘 Need Help?

### Check Documentation

- **Architecture questions**: [ARCHITECTURE.md](./ARCHITECTURE.md)
- **API questions**: [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)
- **Setup issues**: This file's "Common Issues" section
- **Other issues**: [TROUBLESHOOTING.md](./guides/TROUBLESHOOTING.md)

### Debug Information

Get debug info for support:

```bash
# Backend versions
python --version
pip show fastapi uvicorn openai

# Frontend versions
node --version
npm --version
npm list next react

# System info
# macOS:
system_profiler SPSoftwareDataType

# Linux:
uname -a

# Windows:
systeminfo
```

---

## 🎉 Ready to Go!

You now have:
- ✅ Python backend running on port 8000
- ✅ Next.js frontend running on port 3000
- ✅ Database initialized
- ✅ AI agents configured
- ✅ Everything connected

**Next: Visit http://localhost:3000 and create your first job post!**

---

**Last Updated**: November 24, 2025 | **Status**: ✅ Complete
