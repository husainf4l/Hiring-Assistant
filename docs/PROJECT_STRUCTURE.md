# 📁 Project Structure & Organization

## Complete Directory Tree

```
hiring-assistant/
│
├── 📄 README.md                          # Main project overview & quick start
├── 📄 .env                               # Environment variables
├── 📄 .gitignore                         # Git ignore rules
│
├── 📁 backend/                           # FastAPI backend application
│   ├── main.py                           # FastAPI app entry point
│   ├── requirements.txt                  # Python dependencies
│   ├── .env                              # Backend environment variables
│   │
│   ├── 📁 agents/                        # AI Agent modules
│   │   ├── __init__.py
│   │   ├── base.py                       # Base agent class
│   │   ├── interview_agent.py            # Conducts interview questions
│   │   ├── composer_agent.py             # Generates job post content
│   │   ├── formatter_agent.py            # Formats output professionally
│   │   ├── orchestrator.py               # Coordinates all agents
│   │   └── prompts.py                    # AI prompt templates
│   │
│   ├── 📁 integrations/                  # External service integrations
│   │   └── (placeholder for future integrations)
│   │
│   ├── database.py                       # Database connection & setup
│   ├── db_models.py                      # SQLAlchemy database models
│   ├── models.py                         # Pydantic request/response models
│   ├── repositories.py                   # Database operations layer
│   ├── routes.py                         # API endpoints definition
│   │
│   ├── init_db.py                        # Database initialization script
│   ├── hiring_assistant.db               # SQLite database file
│   │
│   └── 📁 __pycache__/                   # Python cache (ignored)
│
├── 📁 frontend/                          # Next.js frontend application
│   ├── package.json                      # Node dependencies
│   ├── tsconfig.json                     # TypeScript configuration
│   ├── next.config.js                    # Next.js configuration
│   │
│   ├── 📁 app/                           # Next.js app directory
│   │   ├── layout.tsx                    # Root layout
│   │   ├── page.tsx                      # Home page
│   │   ├── globals.css                   # Global styles with theme
│   │   │
│   │   └── 📁 dashboard/                 # Dashboard page
│   │       └── page.tsx                  # Dashboard component
│   │
│   ├── 📁 components/                    # React components
│   │   ├── ChatPanel.tsx                 # Chat interface
│   │   ├── PreviewPanel.tsx              # Live job post preview
│   │   └── (future components)
│   │
│   ├── 📁 lib/                           # Utility functions
│   │   └── api.ts                        # API client functions
│   │
│   ├── 📁 types/                         # TypeScript type definitions
│   │   └── index.ts                      # Shared types
│   │
│   └── 📁 node_modules/                  # Node dependencies (ignored)
│
├── 📁 docs/                              # Project documentation
│   ├── PROJECT_STRUCTURE.md              # This file - project layout
│   ├── ARCHITECTURE.md                   # System architecture & design
│   ├── SETUP_GUIDE.md                    # Installation & setup instructions
│   ├── API_DOCUMENTATION.md              # API endpoints reference
│   │
│   ├── 📁 guides/                        # How-to guides
│   │   ├── DEPLOYMENT.md                 # Production deployment
│   │   ├── CONTRIBUTING.md               # Contribution guidelines
│   │   ├── TROUBLESHOOTING.md            # Common issues & solutions
│   │   └── DATABASE.md                   # Database management
│   │
│   ├── 📁 features/                      # Feature documentation
│   │   ├── CHAT_INTERFACE.md             # Chat interface details
│   │   ├── LIVE_PREVIEW.md               # Live preview functionality
│   │   ├── SAVE_FEATURE.md               # Save posts feature
│   │   └── DASHBOARD.md                  # Dashboard feature
│   │
│   └── 📁 technical/                     # Technical deep dives
│       ├── AI_AGENTS.md                  # AI agent logic
│       ├── DATABASE_SCHEMA.md            # Database design
│       └── API_DESIGN.md                 # API architecture
│
├── 📁 scripts/                           # Utility scripts
│   ├── start_backend.sh                  # Start backend server
│   ├── start_frontend.sh                 # Start frontend dev server
│   ├── init_db.py                        # Initialize database
│   └── setup.sh                          # Project setup script
│
├── 📁 config/                            # Configuration files
│   ├── .env.example                      # Example environment variables
│   └── database.yml                      # Database configuration
│
└── 📁 venv/                              # Python virtual environment (ignored)
```

## 📊 Component Organization

### Backend Architecture

```
FastAPI Application
├── API Routes (routes.py)
│   ├── POST /start-chat
│   ├── POST /send-message
│   ├── GET /posts
│   ├── POST /save-post
│   ├── POST /post-preview
│   └── POST /regenerate
│
├── AI Agents (agents/)
│   ├── Interview Agent → Questions
│   ├── Composer Agent → Content
│   └── Formatter Agent → Polish
│
├── Database (database.py)
│   ├── ChatSession model
│   ├── JobPost model
│   └── Repositories
│
└── External Services
    └── OpenAI API
```

### Frontend Architecture

```
Next.js Application
├── Pages
│   ├── Home (page.tsx)
│   │   ├── ChatPanel
│   │   └── PreviewPanel
│   │
│   └── Dashboard (dashboard/page.tsx)
│       ├── Post Grid
│       ├── View Modal
│       └── Actions
│
├── Components (Reusable)
│   ├── ChatPanel
│   ├── PreviewPanel
│   └── (Others)
│
├── Styling (globals.css)
│   ├── Rolevate Theme
│   ├── Responsive Design
│   └── Animations
│
└── API Integration (lib/api.ts)
    ├── Chat endpoints
    ├── Post endpoints
    └── Error handling
```

## 🗂️ File Categories

### Documentation Files
- **README.md** - Main entry point, quick start guide
- **docs/ARCHITECTURE.md** - System design overview
- **docs/SETUP_GUIDE.md** - Installation steps
- **docs/API_DOCUMENTATION.md** - API reference
- **docs/guides/** - How-to guides and troubleshooting
- **docs/features/** - Feature-specific documentation
- **docs/technical/** - Technical deep dives

### Code Files
- **Backend**: Python files in `backend/` and `backend/agents/`
- **Frontend**: TypeScript/React files in `frontend/`
- **Configuration**: Environment and config files

### Configuration Files
- **.env** - Environment variables (not in git)
- **.env.example** - Template for .env
- **backend/requirements.txt** - Python dependencies
- **frontend/package.json** - Node.js dependencies
- **frontend/tsconfig.json** - TypeScript configuration
- **frontend/next.config.js** - Next.js configuration

### Database Files
- **backend/hiring_assistant.db** - SQLite database file
- **backend/db_models.py** - Database schema
- **backend/repositories.py** - Data access layer

### Scripts
- **start_backend.sh** - Backend startup
- **start_frontend.sh** - Frontend startup (create)
- **backend/init_db.py** - Database initialization

## 📝 Key Files by Purpose

### To Start the Project
1. Read: `README.md`
2. Follow: `docs/SETUP_GUIDE.md`
3. Run: `scripts/start_backend.sh` + `scripts/start_frontend.sh`

### To Understand the Architecture
1. Read: `docs/ARCHITECTURE.md`
2. Check: `docs/technical/AI_AGENTS.md`
3. Review: `docs/technical/DATABASE_SCHEMA.md`

### To Use the API
1. Reference: `docs/API_DOCUMENTATION.md`
2. Check: `backend/routes.py`
3. Test: Use provided curl examples

### To Contribute
1. Read: `docs/guides/CONTRIBUTING.md`
2. Follow: `docs/PROJECT_STRUCTURE.md` (this file)
3. Check: `docs/guides/TROUBLESHOOTING.md` if issues

## 🎯 Organization Principles

1. **Clear Separation of Concerns**
   - Backend code in `backend/`
   - Frontend code in `frontend/`
   - Documentation in `docs/`

2. **Logical Grouping**
   - Related code in folders (`agents/`, `components/`)
   - Documentation organized by purpose

3. **Single Responsibility**
   - Each file has one clear purpose
   - Utilities grouped in `lib/` and helper modules

4. **Easy Navigation**
   - Root README points to everything
   - Each folder has purpose in structure
   - Documentation is comprehensive

5. **Scalability**
   - Structure supports adding new features
   - Clear patterns for extensions
   - Room for growth without refactoring

## 🚀 Next Steps

1. ✅ **Setup**: Follow `docs/SETUP_GUIDE.md`
2. ✅ **Understand**: Read `docs/ARCHITECTURE.md`
3. ✅ **Run**: Use scripts in `scripts/` folder
4. ✅ **Develop**: Check `docs/guides/CONTRIBUTING.md`
5. ✅ **Deploy**: See `docs/guides/DEPLOYMENT.md`
