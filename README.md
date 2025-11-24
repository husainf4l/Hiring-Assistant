# HR Hiring Assistant

A simple HR platform where recruiters chat with an AI hiring agent to create professional LinkedIn-style hiring posts.

## 🎯 Core Concept

- **AI Chat Interface**: HR/Recruiters chat naturally with an AI agent
- **Structured Questions**: The agent asks structured questions about the job
- **Live Preview**: A LinkedIn-style hiring post preview updates in real-time as you answer
- **Professional Output**: Generate polished, ready-to-post hiring content
- **Rolevate Integration**: Connects to Rolevate job platform for company data

## 🏗️ Project Structure

```
hiring-assistant/
├── backend/          # FastAPI backend with AI agents
├── frontend/         # Next.js frontend with TypeScript
├── docs/             # API documentation and integration guides
├── .gitignore        # Git ignore rules
├── README.md         # This file
├── start_backend.sh  # Backend startup script
└── test_live_preview.sh # Testing script
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+
- OpenAI API key

### Backend Setup

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp env.example .env
# Edit .env with your OpenAI API key and other settings
```

4. Initialize the database:
```bash
python init_db.py
```

5. Run the server:
```bash
# Using the startup script
../start_backend.sh

# Or manually
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

The application will be available at:
- Frontend: http://localhost:3001
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## ✨ Features

### Core Functionality
- **AI-Powered Interview**: Natural conversation with intelligent AI agent
- **Live Template Preview**: Real-time updates as you answer questions
- **Professional Templates**: LinkedIn-style job post formatting
- **Multi-Agent System**: Specialized agents for different aspects of job creation
- **Job Finder Prototype**: Separate `/job-finder` workspace with live chat + job cards
- **Job Finder API**: `/api/job-finder/*` endpoints for chat + recommendations

### Technical Features
- **FastAPI Backend**: High-performance Python web framework
- **Next.js Frontend**: Modern React framework with TypeScript
- **SQLite Database**: Lightweight, file-based database
- **OpenAI Integration**: GPT-4o-mini for intelligent responses
- **Rolevate API**: GraphQL integration for company and job data
- **Responsive Design**: Works on desktop and mobile devices

### AI Agents
- **Interview Agent**: Conducts structured job interviews
- **Composer Agent**: Creates job descriptions from interview data
- **Formatter Agent**: Formats content into professional templates

## � Configuration

### Environment Variables

Create a `.env` file in the `backend/` directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
ROLEVATE_API_URL=https://rolevate.aqlaan.com/api/graphql
DATABASE_URL=sqlite:///./hiring_assistant.db
```

### Database

The application uses SQLite by default. To initialize:
```bash
cd backend
python init_db.py
```

## 🧪 Testing

Run the live preview test:
```bash
./test_live_preview.sh
```

Test API endpoints:
```bash
# Health check
curl http://localhost:8000/health

# Start chat
curl -X POST http://localhost:8000/api/start-chat \
  -H "Content-Type: application/json" -d '{}'
```

## � API Documentation

When the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🐛 Troubleshooting

### Backend Won't Start
1. Ensure virtual environment is activated
2. Check that all dependencies are installed
3. Verify `.env` file exists with correct API keys

### Frontend Can't Connect
1. Ensure backend is running on port 8000
2. Check CORS settings in backend
3. Verify API endpoints are responding

### Database Issues
1. Delete `hiring_assistant.db` and run `python init_db.py`
2. Check file permissions in the backend directory

## � Documentation

- **API Documentation**: http://localhost:8000/docs (when backend is running)
- **Rolevate Integration Guide**: `docs/ROLEVATE_API_GUIDE.md`
- **Implementation Report**: `docs/ROLEVATE_IMPLEMENTATION_REPORT.md`
- **Job Finder Blueprint**: `backend/JOB_FINDER_PROJECT.md`

