# 🏗️ System Architecture

## Overview

The HR Hiring Assistant is built using a modern three-tier architecture with an AI orchestration layer:

```
┌─────────────────────────────────────────────────────────┐
│                   PRESENTATION LAYER                    │
│                    (Next.js Frontend)                   │
│  Chat Panel  │  Preview Panel  │  Dashboard             │
└───────────────────────┬─────────────────────────────────┘
                        │ HTTP/REST API
                        ↓
┌─────────────────────────────────────────────────────────┐
│                   APPLICATION LAYER                     │
│                    (FastAPI Backend)                    │
│  Routes  │  Agents  │  Business Logic                   │
└───────────────────────┬─────────────────────────────────┘
                        │ AI Processing
                        ↓
┌──────────────────────────────────────────────────────────┐
│                    INTELLIGENCE LAYER                    │
│         Interview Agent  │  Composer  │  Formatter       │
│                  (OpenAI GPT-4o-mini)                    │
└──────────────────────────────────────────────────────────┘
                        │ SQL Queries
                        ↓
┌─────────────────────────────────────────────────────────┐
│                      DATA LAYER                         │
│         SQLite Database  │  Repositories                │
└─────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow

### Complete User Journey

```
1. USER OPENS APP
   │
   ├─ Frontend loads: http://localhost:3000
   ├─ Next.js renders Chat + Preview panels
   └─ User sees empty state

2. USER STARTS CHAT
   │
   ├─ Clicks "Start Creating Post"
   ├─ Frontend: POST /api/start-chat
   ├─ Backend: Creates ChatSession in DB
   ├─ Backend: Interview Agent initializes
   └─ Frontend: First AI question appears

3. USER ANSWERS QUESTION
   │
   ├─ Types response in Chat Panel
   ├─ Clicks "Send"
   ├─ Frontend: POST /api/send-message {user_message}
   │
   ├─ Backend processes:
   │   ├─ Interview Agent: Validates answer
   │   ├─ Composer Agent: Generates post content
   │   ├─ Formatter Agent: Polishes output
   │   ├─ OpenAI API: Calls GPT-4o-mini
   │   └─ Database: Saves state
   │
   ├─ Frontend: GET /api/post-preview
   ├─ Frontend: Updates Preview Panel (real-time)
   └─ Frontend: Shows next question OR complete state

4. REPEAT STEPS 3 (Multiple turns)
   │
   ├─ Each answer refines the post
   ├─ Preview updates live
   ├─ Context accumulates in ChatSession
   └─ Post quality improves

5. USER COMPLETES CHAT
   │
   ├─ No more questions from Interview Agent
   ├─ Complete job post displayed in Preview
   ├─ "Save Post" button appears
   └─ Frontend shows success message

6. USER SAVES POST
   │
   ├─ Clicks "Save Post"
   ├─ Frontend: POST /api/save-post {post_data}
   ├─ Backend: Creates JobPost record in DB
   ├─ Frontend: Auto-redirect to Dashboard
   └─ Dashboard loads with new post

7. USER VIEWS DASHBOARD
   │
   ├─ Frontend: GET /api/posts
   ├─ Backend: Returns all saved posts
   ├─ Frontend: Grid display of posts
   ├─ User can click to view full details
   ├─ User can copy post text
   └─ User can create new post (back to step 2)
```

---

## 🤖 AI Agent Architecture

### Three-Agent Orchestration

```
┌─────────────────────────────────────────────┐
│           Orchestrator (main.py)            │
│  Coordinates all agents and OpenAI calls    │
└──────────────────────────────────────────────┘
         ↙            ↓            ↖
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   Interview  │  │   Composer   │  │  Formatter   │
│    Agent     │  │    Agent     │  │   Agent      │
└──────────────┘  └──────────────┘  └──────────────┘
```

### 1. Interview Agent (`interview_agent.py`)

**Purpose**: Gather job information through conversation

**Workflow**:
```
START
  ↓
Generate Question 1 → User Answer
  ↓
Generate Question 2 → User Answer
  ↓
Generate Question 3 → User Answer
  ↓
... (up to 5-7 questions)
  ↓
Sufficient Info? → YES: Send to Composer
              ↓ NO
          Ask More
```

**Questions Asked**:
1. Job title and position level
2. Key responsibilities
3. Required skills
4. Preferred qualifications
5. Company culture fit
6. Salary range (if applicable)
7. Any special requirements

**Data Collected**: 
- `job_title`: str
- `responsibilities`: list[str]
- `required_skills`: list[str]
- `preferred_qualifications`: list[str]
- `company_info`: str
- `salary_range`: str

### 2. Composer Agent (`composer_agent.py`)

**Purpose**: Generate professional job post content

**Workflow**:
```
Collected Data (from Interview)
  ↓
Analyze Requirements
  ↓
Generate Components:
  ├─ Job Summary
  ├─ Responsibilities (bulleted)
  ├─ Requirements (bulleted)
  ├─ Nice-to-Haves
  └─ Call to Action
  ↓
Combine into Full Post
  ↓
Send to Formatter
```

**Output Structure**:
```json
{
  "job_title": "Senior Full-Stack Engineer",
  "company": "TechCorp",
  "summary": "We're looking for...",
  "responsibilities": ["Build APIs...", "Lead projects..."],
  "requirements": ["5+ years...", "Expert in..."],
  "nice_to_haves": ["MBA...", "Published..."],
  "salary_range": "$120k-150k",
  "call_to_action": "Apply now..."
}
```

### 3. Formatter Agent (`formatter_agent.py`)

**Purpose**: Ensure professional appearance and polish

**Workflow**:
```
Composed Content
  ↓
Check Formatting:
  ├─ Grammar and spelling
  ├─ Tone consistency
  ├─ Length balance
  ├─ Call-to-action clarity
  └─ Formatting consistency
  ↓
Apply Fixes:
  ├─ Correct typos
  ├─ Improve phrasing
  ├─ Add missing sections
  └─ Polish bullet points
  ↓
Final Post
```

**Validates**:
- No grammatical errors
- Professional tone throughout
- Balanced section lengths
- Clear call to action
- Consistent formatting

### Agent Communication Flow

```
User Input
    ↓
┌─────────────────────────────┐
│  Interview Agent            │
│  - Validate answer          │
│  - Decide if more Q needed  │
│  - Extract data             │
└─────────────────────────────┘
    ↓ (if complete)
┌─────────────────────────────┐
│  Composer Agent             │
│  - Generate post content    │
│  - Structure components     │
│  - Create full draft        │
└─────────────────────────────┘
    ↓
┌─────────────────────────────┐
│  Formatter Agent            │
│  - Polish and refine        │
│  - Ensure quality           │
│  - Final check              │
└─────────────────────────────┘
    ↓
Final Job Post
```

---

## 📊 Database Schema

### Tables

#### 1. `chat_sessions` Table
```sql
CREATE TABLE chat_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    messages JSON,  -- Array of messages
    status TEXT,    -- 'active', 'completed'
    job_post_id INTEGER FOREIGN KEY
);
```

**Purpose**: Store conversation history and state

**Columns**:
- `id`: Unique session identifier
- `user_id`: User who started the chat (1 for now)
- `created_at`: When chat started
- `messages`: Full conversation history as JSON
- `status`: Current chat state
- `job_post_id`: Link to generated post (if saved)

#### 2. `job_posts` Table
```sql
CREATE TABLE job_posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    chat_session_id INTEGER FOREIGN KEY,
    title TEXT,
    company TEXT,
    summary TEXT,
    responsibilities TEXT,
    requirements TEXT,
    nice_to_haves TEXT,
    salary_range TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Purpose**: Store saved job posts

**Columns**:
- `id`: Unique post identifier
- `user_id`: User who created (1 for now)
- `chat_session_id`: Reference to chat that created it
- `title`: Job title
- `company`: Company name
- `summary`: Job summary
- `responsibilities`: Responsibilities (JSON array)
- `requirements`: Required qualifications
- `nice_to_haves`: Optional qualifications
- `salary_range`: Salary information
- `created_at`: When post was created
- `updated_at`: Last modification

### ER Diagram

```
┌─────────────────────────┐
│      chat_sessions      │
├─────────────────────────┤
│ id (PK)                 │
│ user_id                 │
│ created_at              │
│ messages (JSON)         │
│ status                  │
│ job_post_id (FK) ─────┐ │
└─────────────────────────┘ │
                            │
                            ↓
                ┌──────────────────────┐
                │    job_posts         │
                ├──────────────────────┤
                │ id (PK)              │
                │ user_id              │
                │ chat_session_id (FK) │
                │ title                │
                │ company              │
                │ summary              │
                │ responsibilities     │
                │ requirements         │
                │ nice_to_haves        │
                │ salary_range         │
                │ created_at           │
                │ updated_at           │
                └──────────────────────┘
```

---

## 🔌 API Endpoints

### Base URL
```
http://localhost:8000/api
```

### Endpoints Summary

| Method | Endpoint | Purpose | Response |
|--------|----------|---------|----------|
| `POST` | `/start-chat` | Initialize chat | `{session_id, first_message}` |
| `POST` | `/send-message` | Send user message | `{ai_response, preview}` |
| `GET` | `/posts` | Get all saved posts | `{posts: []}` |
| `POST` | `/save-post` | Save job post | `{post_id, success}` |
| `POST` | `/post-preview` | Get live preview | `{post_preview}` |
| `POST` | `/regenerate` | Regenerate section | `{regenerated_content}` |

### Detailed Endpoint Documentation

#### 1. POST `/start-chat`

**Request**:
```json
{
  "user_id": 1
}
```

**Response**:
```json
{
  "session_id": 123,
  "first_message": "Hello! I'll help you create a great job posting...",
  "status": "success"
}
```

**Backend Flow**:
```
→ Create ChatSession in DB
→ Initialize Interview Agent
→ Generate first question
→ Store in database
→ Return to frontend
```

#### 2. POST `/send-message`

**Request**:
```json
{
  "session_id": 123,
  "user_message": "Senior Full-Stack Engineer in React and Python"
}
```

**Response**:
```json
{
  "ai_response": "Great! How many years of experience...",
  "preview": {
    "job_title": "Senior Full-Stack Engineer",
    "company": "",
    "responsibilities": [],
    "...": "..."
  },
  "chat_complete": false,
  "status": "success"
}
```

**Backend Flow**:
```
→ Store user message in ChatSession
→ Interview Agent processes answer
→ Composer Agent generates content
→ Formatter Agent polishes
→ Update ChatSession
→ Return response
```

#### 3. GET `/posts`

**Request**: No body, just authentication

**Response**:
```json
{
  "posts": [
    {
      "id": 1,
      "title": "Senior Engineer",
      "company": "TechCorp",
      "created_at": "2025-11-24T10:30:00",
      "preview": "Full job description..."
    }
  ],
  "count": 1,
  "status": "success"
}
```

**Backend Flow**:
```
→ Query JobPosts for user_id
→ Format response
→ Return to frontend
```

#### 4. POST `/save-post`

**Request**:
```json
{
  "session_id": 123,
  "post_data": {
    "title": "Senior Engineer",
    "company": "TechCorp",
    "summary": "...",
    "...": "..."
  }
}
```

**Response**:
```json
{
  "post_id": 456,
  "success": true,
  "message": "Post saved successfully!",
  "status": "success"
}
```

**Backend Flow**:
```
→ Extract data from request
→ Create JobPost record
→ Link to ChatSession
→ Save to database
→ Return post_id
```

---

## 🎨 Frontend Architecture

### Component Hierarchy

```
App (layout.tsx)
├── Header
│   ├── Logo
│   ├── Title
│   └── Dashboard Link
│
├── Main Content
│   ├── ChatPanel
│   │   ├── Messages Container
│   │   │   ├── Message Bubbles (AI)
│   │   │   └── Message Bubbles (User)
│   │   ├── Typing Indicator
│   │   └── Input Area
│   │       ├── Text Input
│   │       └── Send Button
│   │
│   └── PreviewPanel
│       ├── Preview Header
│       ├── Preview Content
│       │   ├── Job Title
│       │   ├── Company
│       │   ├── Responsibilities
│       │   ├── Requirements
│       │   └── Salary
│       └── Action Buttons
│           ├── Copy Button
│           ├── Regenerate
│           └── Save Button
│
└── Dashboard Page
    ├── Header
    ├── Post Grid
    │   └── Post Cards (multiple)
    │       ├── Title
    │       ├── Company
    │       ├── Preview
    │       └── View Button
    │
    └── Modal (for details)
        ├── Full Post Content
        ├── Copy Button
        ├── Close Button
        └── Actions
```

### State Management

```
Frontend State:
├── Chat State
│   ├── messages: Message[]
│   ├── session_id: number
│   ├── loading: boolean
│   └── chat_complete: boolean
│
├── Preview State
│   ├── current_post: JobPost
│   ├── preview_html: string
│   └── last_updated: timestamp
│
├── Dashboard State
│   ├── posts: JobPost[]
│   ├── selected_post: JobPost | null
│   ├── modal_open: boolean
│   └── loading: boolean
│
└── UI State
    ├── theme: string
    ├── responsive: boolean
    └── animations_enabled: boolean
```

### Data Flow (Frontend)

```
User Interaction
    ↓
Component Updates State
    ↓
Effect Hook Triggered
    ↓
API Call (lib/api.ts)
    ↓
Request to Backend
    ↓
Response Received
    ↓
State Updated with Response
    ↓
Component Re-renders
    ↓
User Sees Update
```

---

## 🔒 Security Considerations

### Current Implementation
- ✅ CORS enabled (localhost only)
- ✅ Input validation on backend
- ✅ SQL injection protection (SQLAlchemy ORM)
- ⚠️ No authentication (placeholder user_id = 1)

### For Production
1. **Add JWT Authentication**
   - User login/register
   - Token validation on each request
   - Token refresh mechanism

2. **Add Authorization**
   - User can only access their own posts
   - Role-based access control

3. **Add Rate Limiting**
   - Prevent API abuse
   - Limit OpenAI API calls

4. **Add Input Validation**
   - Sanitize user input
   - Validate data types and lengths

5. **Add HTTPS**
   - SSL/TLS certificates
   - Secure cookies

---

## 🚀 Deployment Architecture

### Development Environment
```
Local Machine
├── Backend: http://localhost:8000
├── Frontend: http://localhost:3000
└── Database: SQLite file
```

### Production Environment
```
AWS/Cloud Server
├── Backend: FastAPI on Gunicorn
├── Frontend: Next.js on Node.js
├── Database: PostgreSQL
├── Reverse Proxy: Nginx
├── SSL: Let's Encrypt
└── Monitoring: CloudWatch
```

---

## 📈 Performance Considerations

### Optimizations Implemented
- ✅ Lazy loading of components
- ✅ Efficient database queries
- ✅ Caching strategies
- ✅ Optimized CSS

### Areas for Improvement
- 📋 Add database indexes
- 📋 Implement Redis caching
- 📋 Add CDN for static assets
- 📋 Optimize API response times
- 📋 Add request compression

---

## 🔄 Extensibility

### Adding New Features

**Example: Export to PDF**
```
1. Add new endpoint: POST /export-post
2. Create ExportAgent in agents/
3. Add export utility in lib/
4. Add button to PreviewPanel
5. Test and document
```

**Example: Email Integration**
```
1. Add email service configuration
2. Create EmailService class
3. Add POST /send-email endpoint
4. Add email template files
5. Integrate with save flow
```

---

## 📚 Architecture Principles

1. **Separation of Concerns**
   - Backend handles business logic
   - Frontend handles UI/UX
   - Agents handle AI coordination

2. **Scalability**
   - Stateless API design
   - Database as single source of truth
   - Easy horizontal scaling

3. **Maintainability**
   - Clear code organization
   - Well-documented functions
   - Consistent patterns

4. **Testability**
   - Isolated components
   - Mockable dependencies
   - Clear interfaces

---

## 🎯 Summary

The HR Hiring Assistant uses a modern, scalable architecture with:
- **Three-tier structure** (Presentation, Application, Data)
- **AI orchestration** with specialized agents
- **RESTful API** for client-server communication
- **Real-time updates** via polling/websockets
- **Professional design** with responsive layout
- **Scalable database** schema

This architecture supports current features and allows for easy expansion as the product grows.

---

**For more details, see the complete documentation in `/docs`**
