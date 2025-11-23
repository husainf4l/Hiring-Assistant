# HR Hiring Assistant

A simple HR platform where recruiters chat with an AI hiring agent to create professional LinkedIn-style hiring posts.

## 🎯 Core Concept

- **AI Chat Interface**: HR/Recruiters chat naturally with an AI agent
- **Structured Questions**: The agent asks structured questions about the job
- **Live Preview**: A LinkedIn-style hiring post preview updates in real-time as you answer
- **Professional Output**: Generate polished, ready-to-post hiring content

## 🏗️ Project Structure

```
hiring-assistant/
├── backend/          # FastAPI backend
├── frontend/         # Next.js frontend
├── venv/            # Python virtual environment
└── PROJECT_PHASES.md # Project documentation
```

## 🚀 Quick Start

### Backend Setup

1. Activate virtual environment:
```bash
source venv/bin/activate
```

2. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your OpenAI API key
```

4. Run the server:
```bash
# Option 1: Using the startup script
../start_backend.sh

# Option 2: Manual start
cd backend
source ../venv/bin/activate
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Run the development server:
```bash
npm run dev
```

## 📋 Features (Phase 1 - Foundation)

- ✅ Project structure setup
- ✅ FastAPI backend foundation
- ✅ Next.js frontend foundation
- ✅ Data models defined
- ✅ Basic configuration files

## 🔄 Next Steps

See `PROJECT_PHASES.md` for detailed implementation phases.

## 📚 Documentation

- **PROJECT_PHASES.md** - Detailed project phases and implementation plan
- **ARCHITECTURE_AND_DOCUMENTATION.md** - Complete architecture, prompts, database flow, task lists, user flows, and wireframes

## 📝 License

MIT

