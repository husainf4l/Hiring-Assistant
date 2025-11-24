# 🎯 HR Hiring Assistant

> **Professional AI-Powered Job Post Generator** using FastAPI, Next.js, and OpenAI

A modern SaaS application that helps HR professionals and recruiters create compelling job postings through an intelligent AI chat interface with real-time live preview.

---

## 📚 Quick Navigation

| Section | Purpose | Link |
|---------|---------|------|
| 🚀 **Getting Started** | Setup & run locally | [SETUP_GUIDE.md](./docs/guides/SETUP_GUIDE.md) |
| 🏗️ **Architecture** | System design & flow | [ARCHITECTURE.md](./docs/ARCHITECTURE.md) |
| 📂 **Project Structure** | File organization | [PROJECT_STRUCTURE.md](./docs/PROJECT_STRUCTURE.md) |
| 🔌 **API Reference** | Endpoints & payloads | [API_DOCUMENTATION.md](./docs/API_DOCUMENTATION.md) |
| 🤖 **AI Agents** | How agents work | [AI_AGENTS.md](./docs/technical/AI_AGENTS.md) |
| 🗄️ **Database** | Schema & models | [DATABASE_SCHEMA.md](./docs/technical/DATABASE_SCHEMA.md) |
| 🐛 **Troubleshooting** | Common issues | [TROUBLESHOOTING.md](./docs/guides/TROUBLESHOOTING.md) |
| 🚢 **Deployment** | Production setup | [DEPLOYMENT.md](./docs/guides/DEPLOYMENT.md) |

---

## ⚡ Quick Start (5 minutes)

### Prerequisites
- Python 3.8+ with pip
- Node.js 16+ with npm
- OpenAI API key

### 1️⃣ Clone & Setup Backend

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### 2️⃣ Initialize Database

```bash
python init_db.py
```

### 3️⃣ Start Backend Server

```bash
cd ..
./scripts/start_backend.sh
# Or manually: uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

✅ Backend running on: **http://localhost:8000**

### 4️⃣ Setup & Start Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

✅ Frontend running on: **http://localhost:3000**

### 5️⃣ Open & Use

Visit **http://localhost:3000** in your browser! 🎉

---

## 🎨 Key Features

### 💬 Intelligent Chat Interface
- **Real-time AI conversation** with job posting guidance
- **Multi-turn dialogue** for comprehensive job information gathering
- **Context-aware responses** that improve post quality

### 👁️ Live Preview Panel
- **Real-time updates** as you chat
- **Professional formatting** applied instantly
- **Copy to clipboard** for quick sharing
- **Regenerate sections** for refinement

### 💾 Save & Dashboard
- **One-click save** to persist job posts
- **Dashboard view** to manage all posts
- **Modal details** for full post viewing
- **Post management** (view, copy, export)

### 🤖 Three-Agent AI System
- **Interview Agent** - Asks clarifying questions
- **Composer Agent** - Generates professional content
- **Formatter Agent** - Ensures professional appearance

### 🎨 Professional Design
- **Rolevate-inspired theme** with modern aesthetics
- **Responsive layout** for all devices
- **Smooth animations** and transitions
- **Accessible UI** with proper contrast and keyboard support

---

## 📂 Project Organization

```
hiring-assistant/
├── 📄 README.md                 ← You are here
├── 🔑 .env                      ← Environment variables
│
├── 📁 backend/                  ← FastAPI application
│   ├── main.py                  ← Entry point
│   ├── routes.py                ← API endpoints
│   ├── requirements.txt          ← Python dependencies
│   └── agents/                  ← AI agents
│
├── 📁 frontend/                 ← Next.js application
│   ├── app/                     ← Pages
│   ├── components/              ← React components
│   ├── package.json             ← Node dependencies
│   └── app/globals.css          ← Global styles
│
├── 📁 docs/                     ← Full documentation
│   ├── ARCHITECTURE.md
│   ├── SETUP_GUIDE.md
│   ├── API_DOCUMENTATION.md
│   ├── guides/                  ← How-to guides
│   ├── features/                ← Feature docs
│   └── technical/               ← Technical dives
│
└── 📁 scripts/                  ← Utility scripts
    └── start_backend.sh
```

👉 **[See Full Structure](./docs/PROJECT_STRUCTURE.md)**

---

## 🔧 Technology Stack

### Backend
- **Framework**: FastAPI (Python web framework)
- **Server**: Uvicorn (ASGI server)
- **Database**: SQLite with SQLAlchemy ORM
- **AI**: OpenAI GPT-4o-mini API
- **Architecture**: MVC with Agent pattern

### Frontend
- **Framework**: Next.js 14 (React meta-framework)
- **Language**: TypeScript for type safety
- **Styling**: CSS with Rolevate theme
- **API Client**: Axios/Fetch integration
- **State**: React hooks

### Infrastructure
- **Version Control**: Git & GitHub
- **Environment**: Python venv + Node.js npm
- **Database**: SQLite (dev), PostgreSQL (prod)

---

## 🚀 API Overview

All endpoints are prefixed with `http://localhost:8000/api/`

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `POST` | `/start-chat` | Initialize new chat session |
| `POST` | `/send-message` | Send user message to chat |
| `GET` | `/posts` | Get all saved job posts |
| `POST` | `/save-post` | Save job post to database |
| `POST` | `/post-preview` | Get live post preview |
| `POST` | `/regenerate` | Regenerate post section |

📖 **[Full API Reference](./docs/API_DOCUMENTATION.md)**

---

## 📊 System Architecture

### High-Level Flow

```
User Message
    ↓
Chat Interface
    ↓
FastAPI Backend
    ↓
Interview Agent (asks questions)
    ↓
Composer Agent (generates content)
    ↓
Formatter Agent (polishes)
    ↓
OpenAI API (GPT-4o-mini)
    ↓
Response
    ↓
Database Save
    ↓
Live Preview Update
    ↓
User Sees Result
```

### Component Interaction

```
┌─────────────────────────────────────────┐
│         Frontend (Next.js)              │
├──────────────┬──────────────────────────┤
│ Chat Panel   │  Preview Panel           │
└──────────────┴──────────────────────────┘
       ↓
┌─────────────────────────────────────────┐
│      API Routes (FastAPI)               │
│  /start-chat, /send-message, /save-post │
└─────────────────────────────────────────┘
       ↓
┌─────────────────────────────────────────┐
│       AI Agent Orchestrator             │
├─────────────┬──────────────┬────────────┤
│ Interview   │ Composer     │ Formatter  │
└─────────────┴──────────────┴────────────┘
       ↓
┌─────────────────────────────────────────┐
│      OpenAI GPT-4o-mini API             │
└─────────────────────────────────────────┘
       ↓
┌─────────────────────────────────────────┐
│      SQLite Database                    │
│  (Chat Sessions & Job Posts)            │
└─────────────────────────────────────────┘
```

👉 **[Full Architecture Diagram](./docs/ARCHITECTURE.md)**

---

## 📖 Documentation

Complete documentation is available in the `docs/` folder:

### Getting Started
- **[SETUP_GUIDE.md](./docs/guides/SETUP_GUIDE.md)** - Installation & configuration
- **[TROUBLESHOOTING.md](./docs/guides/TROUBLESHOOTING.md)** - Common issues & solutions

### Understanding the System
- **[ARCHITECTURE.md](./docs/ARCHITECTURE.md)** - System design & data flow
- **[PROJECT_STRUCTURE.md](./docs/PROJECT_STRUCTURE.md)** - File organization
- **[API_DOCUMENTATION.md](./docs/API_DOCUMENTATION.md)** - Complete API reference

### Features
- **[Chat Interface](./docs/features/CHAT_INTERFACE.md)** - How the chat works
- **[Live Preview](./docs/features/LIVE_PREVIEW.md)** - Real-time updates
- **[Save Feature](./docs/features/SAVE_FEATURE.md)** - Saving posts
- **[Dashboard](./docs/features/DASHBOARD.md)** - Managing posts

### Technical Deep Dives
- **[AI_AGENTS.md](./docs/technical/AI_AGENTS.md)** - Agent architecture
- **[DATABASE_SCHEMA.md](./docs/technical/DATABASE_SCHEMA.md)** - Database design
- **[API_DESIGN.md](./docs/technical/API_DESIGN.md)** - API patterns

### Deployment & Contribution
- **[DEPLOYMENT.md](./docs/guides/DEPLOYMENT.md)** - Production setup
- **[CONTRIBUTING.md](./docs/guides/CONTRIBUTING.md)** - How to contribute

---

## 🎯 Common Tasks

### Run the Full Application
```bash
# Terminal 1: Start backend
./scripts/start_backend.sh

# Terminal 2: Start frontend
cd frontend && npm run dev
```

### Initialize Fresh Database
```bash
cd backend
python init_db.py
```

### Check Health Status
```bash
# Backend health
curl http://localhost:8000/health

# Frontend
curl http://localhost:3000
```

### View Database
```bash
sqlite3 backend/hiring_assistant.db
```

### Run Tests
```bash
cd backend
pytest test_routes.py
```

---

## 🔒 Environment Variables

Create a `.env` file in the `backend/` folder:

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-...your-api-key-here...

# Database
DATABASE_URL=sqlite:///./hiring_assistant.db

# Server
API_HOST=0.0.0.0
API_PORT=8000
```

👉 **[Environment Setup Guide](./docs/guides/SETUP_GUIDE.md#-environment-configuration)**

---

## 📊 Current Status

| Component | Status | Details |
|-----------|--------|---------|
| 🔷 Backend API | ✅ Running | FastAPI on port 8000 |
| 🔷 Frontend | ✅ Running | Next.js on port 3000 |
| 💾 Database | ✅ Initialized | SQLite with models |
| 🤖 AI Agents | ✅ Working | Interview, Composer, Formatter |
| 🎨 Design | ✅ Complete | Rolevate theme applied |
| 📚 Documentation | ✅ Comprehensive | 2000+ lines |
| 🧪 Testing | ✅ Available | Test files included |
| 🚀 Production Ready | ⏳ Auth needed | Add JWT before deploy |

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](./docs/guides/CONTRIBUTING.md) for guidelines.

### Before Contributing
1. Read the [ARCHITECTURE.md](./docs/ARCHITECTURE.md)
2. Check [PROJECT_STRUCTURE.md](./docs/PROJECT_STRUCTURE.md)
3. Follow [CONTRIBUTING.md](./docs/guides/CONTRIBUTING.md)
4. Run tests before submitting PR

---

## 🐛 Issues & Support

### Common Issues
See **[TROUBLESHOOTING.md](./docs/guides/TROUBLESHOOTING.md)** for solutions to common problems.

### Getting Help
1. Check the documentation in `docs/`
2. Review [TROUBLESHOOTING.md](./docs/guides/TROUBLESHOOTING.md)
3. Check GitHub issues
4. Create a new issue with details

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 📞 Contact & Support

For questions or support:
- 📧 Email: support@example.com
- 💬 Issues: GitHub Issues
- 📖 Docs: See `/docs` folder

---

## 🎉 Ready to Get Started?

**👉 [Go to Setup Guide](./docs/guides/SETUP_GUIDE.md)**

Or jump right in:
```bash
./scripts/start_backend.sh  # Terminal 1
cd frontend && npm run dev  # Terminal 2
```

Visit **http://localhost:3000** and start creating job posts! 🚀

---

## 🗺️ Project Roadmap

### ✅ Phase 1: Core Features (Complete)
- Chat interface
- AI agents
- Live preview
- Save & dashboard

### 📋 Phase 2: Enhancements (Future)
- User authentication
- Multiple templates
- Advanced analytics
- Export options

### 🔮 Phase 3: Scaling (Future)
- Multi-language support
- API for third-party integrations
- Enterprise features
- Advanced reporting

---

**Last Updated**: November 24, 2025 | **Status**: ✅ Complete & Organized
