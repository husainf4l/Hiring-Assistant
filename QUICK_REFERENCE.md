# Save Post Feature - Quick Reference Guide

## 🎯 User Journey

### Homepage (Create Post)
```
┌─────────────────────────────────────────────────────────────┐
│  HR Hiring Assistant              [View Dashboard] Button    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────┐              ┌──────────────────────┐ │
│  │  Left Panel      │              │  Right Panel         │ │
│  │  Chat Interface  │              │  Live Preview        │ │
│  │                  │              │                      │ │
│  │  You: Tell me    │              │  [Complete Badge]    │ │
│  │  about...        │              │  Job Title           │ │
│  │                  │              │  Company Details     │ │
│  │  AI: Please      │              │  Summary             │ │
│  │  provide...      │              │  Responsibilities    │ │
│  │                  │              │                      │ │
│  │  [Text Input]    │              │  [Save Post Button]  │ ← When complete
│  │  [Send Button]   │              │  [Copy Button]       │
│  └──────────────────┘              └──────────────────────┘ │
│                                                               │
└─────────────────────────────────────────────────────────────┘

Styling:
- Gradient background (white → light blue)
- Indigo buttons with hover elevation
- Smooth transitions
- Professional typography
```

### Save Flow
```
User Completes Chat
        ↓
Chat Status: isComplete = true
        ↓
Save Button Appears (Indigo Gradient)
        ↓
User Clicks "Save Post"
        ↓
Button Shows "Saving..." State
        ↓
POST /api/save-post
{
  "session_id": "uuid...",
  "user_id": 1
}
        ↓
Backend Saves to Database
        ↓
Response: { message, job_post }
        ↓
Success Alert Shown
        ↓
Auto-Redirect to /dashboard (500ms)
        ↓
Dashboard Loads Saved Posts
```

### Dashboard (View Saved Posts)
```
┌─────────────────────────────────────────────────────────────┐
│  Saved Hiring Posts                   [Create New Post]     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────┐  ┌──────────────────────┐         │
│  │  Post Card           │  │  Post Card           │         │
│  │                      │  │                      │         │
│  │  Senior Dev Engineer │  │  Product Manager     │         │
│  │                      │  │                      │         │
│  │  We are looking for  │  │  Join our growing    │         │
│  │  an experienced...   │  │  product team...     │         │
│  │                      │  │                      │         │
│  │  Nov 24, 2025       │  │  Nov 24, 2025       │         │
│  │                      │  │                      │         │
│  │  [View] [Copy]      │  │  [View] [Copy]      │         │
│  └──────────────────────┘  └──────────────────────┘         │
│                                                               │
│  ┌──────────────────────┐                                    │
│  │  Post Card           │                                    │
│  │  ...                 │                                    │
│  └──────────────────────┘                                    │
│                                                               │
└─────────────────────────────────────────────────────────────┘

Styling:
- Gradient header with text effect
- Post cards with subtle borders
- Card elevation on hover (+4px translateY)
- Indigo buttons
- Professional spacing
```

### Modal (View Full Post)
```
┌────────────────────────────────────────────────────────────┐
│  Senior Dev Engineer                            [Close ×]   │
├────────────────────────────────────────────────────────────┤
│                                                              │
│  SUMMARY                                                     │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ We are looking for an experienced senior software...  │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  RESPONSIBILITIES                                            │
│  • Design and architect scalable systems                     │
│  • Lead technical discussions and code reviews              │
│  • Mentor junior developers                                 │
│                                                              │
│  REQUIREMENTS                                                │
│  • 5+ years of software development                         │
│  • Strong system design skills                              │
│  • Experience with microservices                            │
│                                                              │
│  SKILLS                                                      │
│  [Python] [Java] [React] [PostgreSQL] [Docker]             │
│                                                              │
│  [Copy to Clipboard Button]                                 │
│                                                              │
└────────────────────────────────────────────────────────────┘

Styling:
- Backdrop blur effect
- Rounded corners
- Gradient backgrounds
- Indigo section headers
- Professional typography
```

## 🔧 Technical Flow

### Frontend State Management
```
Home Component (page.tsx)
├── useState: sessionId
├── useState: messages[]
├── useState: jobPost
├── useState: isComplete
├── useState: isLoading
└── useEffect: Initialize chat
    └── startChat() API call

PreviewPanel Component
├── Props: jobPost, isComplete, sessionId
├── useState: isSaving
├── handleSave()
│   ├── Validate sessionId
│   ├── Call savePost() API
│   ├── Show success alert
│   └── router.push('/dashboard') ← REDIRECT
└── Render: Preview + Buttons

Dashboard Component
├── useState: posts[], isLoading, selectedPost
├── useEffect: loadPosts()
│   ├── getPosts(userId) API call
│   └── setPosts(response.posts)
└── Render: Posts Grid + Modal
```

### Backend Data Flow
```
FastAPI Router (/api/save-post)
└── POST /save-post
    ├── Validate session_id
    ├── Get chat_session from DB
    ├── Get job_post_id from session
    ├── Get job_post from DB
    ├── Update user_id if needed
    ├── Convert to Pydantic model
    └── Return { message, job_post }

GET /api/posts?user_id=1
└── Query job_posts WHERE user_id = 1
    └── Return { posts[], total }
```

### Database Tables
```
job_posts (SQLite)
├── id (Primary Key)
├── user_id (Foreign Key)
├── title
├── summary
├── company
├── responsibilities (JSON)
├── requirements (JSON)
├── skills (JSON)
├── keywords (JSON)
├── hashtags (JSON)
├── workplace_type
├── location
├── job_type
├── tone_type
├── culture_and_team
├── compensation_benefits
├── call_to_action
├── created_at
└── updated_at

Example Row:
{
  id: 1,
  user_id: 1,
  title: "Senior Developer",
  created_at: "2025-11-24T10:30:00Z",
  ...
}
```

## 🎨 UI Component Hierarchy

```
Home
├── TopBar
│   ├── Title: "HR Hiring Assistant"
│   └── Button: "View Dashboard"
└── PanelsWrapper
    ├── LeftPanel
    │   └── ChatPanel
    │       ├── Messages
    │       ├── InputForm
    │       └── SendButton
    └── RightPanel
        └── PreviewPanel
            ├── Preview Header
            ├── JobPostPreview
            ├── Sections (Summary, Responsibilities, etc.)
            └── ActionButtons
                ├── SaveButton ← Triggers save + redirect
                └── CopyButton

Dashboard
├── DashboardHeader
│   ├── Title: "Saved Hiring Posts"
│   └── Button: "Create New Post"
├── PostsGrid
│   └── PostCard[] (Repeating)
│       ├── Title
│       ├── Summary Preview
│       ├── Date
│       └── ActionButtons
│           ├── ViewButton → Opens Modal
│           └── CopyButton
└── PostViewModal (When viewing)
    ├── ModalHeader
    │   ├── Title
    │   └── CloseButton
    └── PostView
        ├── Section[] (Repeating)
        │   └── Content
        └── CopyButton
```

## 📊 API Request/Response Examples

### 1. Start Chat
```
Request:
POST /api/start-chat
{
  "user_id": 1
}

Response (200 OK):
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "response": "Hello! I'll help you create a compelling job posting...",
  "is_complete": false,
  "job_post": null
}
```

### 2. Send Message
```
Request:
POST /api/send-message
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Senior Software Engineer"
}

Response (200 OK):
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "response": "Great! What company is this position for?",
  "is_complete": false,
  "job_post": {
    "title": "Senior Software Engineer",
    "summary": null,
    ...
  }
}
```

### 3. Save Post ← KEY ENDPOINT
```
Request:
POST /api/save-post
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": 1
}

Response (200 OK):
{
  "message": "Post saved successfully",
  "job_post": {
    "id": 1,
    "user_id": 1,
    "title": "Senior Software Engineer",
    "summary": "We are looking for...",
    "company": "Tech Corp",
    "responsibilities": [
      "Design and architect systems",
      "Lead code reviews",
      "Mentor team members"
    ],
    "requirements": [
      "5+ years experience",
      "Strong system design",
      "Communication skills"
    ],
    "skills": ["Python", "JavaScript", "React"],
    "keywords": ["backend", "frontend", "fullstack"],
    "hashtags": ["hiring", "developers", "careers"],
    "created_at": "2025-11-24T10:30:00Z",
    "updated_at": "2025-11-24T10:30:00Z"
  }
}
```

### 4. Get Saved Posts
```
Request:
GET /api/posts?user_id=1&skip=0&limit=100

Response (200 OK):
{
  "posts": [
    {
      "id": 1,
      "user_id": 1,
      "title": "Senior Software Engineer",
      "summary": "We are looking for...",
      ...
    },
    {
      "id": 2,
      "user_id": 1,
      "title": "Product Manager",
      ...
    }
  ],
  "total": 2
}
```

## ⚡ Key Features

### Save Button
- Appears only when `isComplete === true`
- Shows "Saving..." during operation
- Indigo gradient background (#6366f1 → #4f46e5)
- Box shadow for elevation (0 4px 12px)
- Hover effect: Lifts up 2px with enhanced shadow

### Redirect
- Automatic 500ms delay after success
- Smooth transition to dashboard
- Session preserved (fresh data loaded)

### Dashboard Cards
- Responsive grid (auto-fill, minmax 320px)
- Subtle borders and shadows
- 4px elevation on hover
- Gradient text for titles
- Date display formatted
- Quick action buttons (View, Copy)

### Professional Design
- Gradient backgrounds throughout
- Indigo primary color scheme
- Smooth transitions (0.2-0.3s ease)
- Proper spacing and padding
- Readable typography
- Accessible color contrasts

## 🚀 Quick Commands

### Run Backend
```bash
cd /home/husain/hiring-assistant
source venv/bin/activate
cd backend
python -m uvicorn main:app --reload --port 8000
```

### Run Frontend
```bash
cd /home/husain/hiring-assistant/frontend
npm run dev
```

### Access Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api
- Dashboard: http://localhost:3000/dashboard

### Test Save Feature
1. Navigate to http://localhost:3000
2. Complete chat conversation
3. Click "Save Post"
4. Verify redirect to dashboard
5. See post in grid

### Check Database
```bash
sqlite3 /home/husain/hiring-assistant/hiring_assistant.db
SELECT * FROM job_posts;
```

## 📝 Environment Setup

### Required Files
- `.env.example` → `.env` (Backend)
- `.env.local` (Frontend for API URL)

### Environment Variables
```
# Backend
OPENAI_API_KEY=sk-...
DATABASE_URL=sqlite:///hiring_assistant.db

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

## ✅ Verification Checklist

- [ ] Backend running at http://localhost:8000
- [ ] Frontend running at http://localhost:3000
- [ ] Health check passing: `curl http://localhost:8000/health`
- [ ] Chat initializes on page load
- [ ] Messages display correctly
- [ ] Preview updates in real-time
- [ ] Save button appears when complete
- [ ] Save operation completes in <3 seconds
- [ ] Redirect to dashboard works
- [ ] Post appears on dashboard
- [ ] Dashboard displays all saved posts
- [ ] View modal opens and displays post
- [ ] Copy to clipboard works
- [ ] No console errors
- [ ] Responsive on mobile/tablet

## 📞 Support Contacts

For issues or questions:
1. Check TESTING_SAVE_FEATURE.md for detailed troubleshooting
2. Check console for error messages (F12 → Console)
3. Verify both backend and frontend are running
4. Review API responses in Network tab (F12 → Network)

---

**Status**: ✅ Implementation Complete
**Version**: 1.0
**Last Updated**: November 24, 2025
