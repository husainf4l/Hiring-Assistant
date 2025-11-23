# HR Hiring Assistant — Complete Architecture & Documentation

## 🚀 PHASE 1 — System Architecture Diagram

### Architecture Overview (WebSocket-Based)

```
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND LAYER (Next.js)                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Chat UI    │  │ Live Preview │  │  Dashboard   │         │
│  │              │  │    Panel    │  │              │         │
│  │ - Messages   │  │ - Title      │  │ - Post List  │         │
│  │ - Input      │  │ - Summary    │  │ - View/Edit  │         │
│  │ - Typing     │  │ - Sections   │  │ - Copy       │         │
│  │ - WebSocket  │  │ - Real-time  │  │ - REST API   │         │
│  │   Client     │  │   Updates    │  │   (for CRUD) │         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
│         │                 │                  │                  │
│  ┌──────┴─────────────────┴──────────────────┴──────┐        │
│  │         Authentication Pages (JWT)                 │        │
│  │         - Login / Signup (REST API)                 │        │
│  └────────────────────────────────────────────────────┘        │
│                                                                   │
└───────────────────────────┬─────────────────────────────────────┘
                              │
                              │ WebSocket Connection (ws://)
                              │ Real-time bidirectional
                              │
┌─────────────────────────────▼─────────────────────────────────────┐
│                  BACKEND LAYER (FastAPI)                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │         WebSocket Connection Manager                       │    │
│  │  - ws://server/chat/{session_id}                          │    │
│  │  - Connection handling                                     │    │
│  │  - Message routing                                         │    │
│  │  - Client session tracking                                 │    │
│  └──────────────────────┬─────────────────────────────────────┘    │
│                         │                                           │
│  ┌──────────────────────▼─────────────────────────────────────┐    │
│  │         WebSocket Message Handler                           │    │
│  │  - on_connect: Initialize session                          │    │
│  │  - on_message: Process user messages                       │    │
│  │  - on_disconnect: Cleanup session                          │    │
│  │  - Broadcast: Send updates to client                       │    │
│  └──────────────────────┬─────────────────────────────────────┘    │
│                         │                                           │
│  ┌──────────────────────▼─────────────────────────────────────┐    │
│  │         AI Orchestration Layer                             │    │
│  │  - Session Management                                      │    │
│  │  - Agent Coordination                                      │    │
│  │  - State Management                                        │    │
│  │  - Streaming responses                                     │    │
│  └──────────────────────┬─────────────────────────────────────┘    │
│                         │                                           │
│  ┌──────────────────────▼─────────────────────────────────────┐    │
│  │         REST API Endpoints (for non-realtime)              │    │
│  │  - POST /api/save-post (save completed post)              │    │
│  │  - GET  /api/posts (list saved posts)                     │    │
│  │  - POST /api/regenerate-section (regenerate)              │    │
│  │  - GET  /api/post/{id} (get saved post)                   │    │
│  └──────────────────────┬─────────────────────────────────────┘    │
│                         │                                           │
│  ┌──────────────────────▼─────────────────────────────────────┐    │
│  │         Auth Service (JWT)                                 │    │
│  │  - User Authentication (REST)                             │    │
│  │  - Token Management                                        │    │
│  │  - WebSocket connection validation                         │    │
│  └──────────────────────┬─────────────────────────────────────┘    │
│                         │                                           │
└──────────────────────────┼──────────────────────────────────────────┘
                            │
                            │
┌───────────────────────────▼──────────────────────────────────────────┐
│                      AI LAYER (LLM)                                   │
├───────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐│
│  │ Interview Agent  │  │ Post Composer    │  │ Formatter Agent  ││
│  │                  │  │ Agent            │  │                  ││
│  │ - Questions      │  │ - Title Gen      │  │ - Grammar        ││
│  │ - Data Collection│  │ - Summary        │  │ - Structure      ││
│  │ - Completion     │  │ - Sections       │  │ - Formatting     ││
│  │ - Streaming      │  │ - Streaming      │  │ - Streaming      ││
│  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘│
│           │                     │                      │          │
│  ┌────────┴─────────────────────┴──────────────────────┴────────┐│
│  │         Context / Memory Manager                               ││
│  │  - Conversation History                                        ││
│  │  - Job Information Extraction                                  ││
│  │  - Session State                                               ││
│  │  - Real-time state updates                                     ││
│  └───────────────────────────────────────────────────────────────┘│
│                                                                      │
└───────────────────────────┬────────────────────────────────────────┘
                             │
                             │
┌─────────────────────────────▼────────────────────────────────────────┐
│              DATABASE LAYER (PostgreSQL)                              │
├──────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                │
│  │    users     │  │   sessions   │  │  job_posts  │                │
│  │              │  │              │  │             │                │
│  │ - id         │  │ - id         │  │ - id         │                │
│  │ - email      │  │ - user_id    │  │ - user_id    │                │
│  │ - password   │  │ - is_complete│  │ - title      │                │
│  │ - company    │  │ - created_at │  │ - summary    │                │
│  └──────┬───────┘  └──────┬───────┘  │ - sections   │                │
│         │                 │           └──────┬───────┘                │
│         │                 │                  │                         │
│  ┌──────┴─────────────────┴──────────────────┴──────┐               │
│  │              messages                              │               │
│  │  - id, session_id, sender, content, created_at    │               │
│  └───────────────────────────────────────────────────┘               │
│                                                                        │
│  Relationships:                                                       │
│  users (1) ──→ (many) job_posts                                       │
│  users (1) ──→ (many) sessions                                        │
│  sessions (1) ──→ (many) messages                                    │
│  sessions (1) ──→ (1) job_posts (when complete)                      │
│                                                                        │
└──────────────────────────────────────────────────────────────────────┘
```

### WebSocket Communication Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    WEBSOCKET DATA FLOW                            │
└─────────────────────────────────────────────────────────────────┘

1. CONNECTION ESTABLISHMENT
   │
   Frontend: ws.connect('ws://server/chat/{session_id}')
   │
   ▼
   Backend: WebSocket Connection Manager
   │
   ├─→ Validate JWT token
   ├─→ Create/retrieve session
   ├─→ Register client connection
   └─→ Send: { type: 'connected', session_id: '...' }
   │
   ▼
   Frontend: Connection established, ready to send/receive

2. USER SENDS MESSAGE
   │
   Frontend: ws.send({
     type: 'user_message',
     content: 'Software Engineer',
     session_id: '...'
   })
   │
   ▼
   Backend: WebSocket Message Handler receives
   │
   ├─→ Store message in database
   ├─→ Send typing indicator: { type: 'typing', status: true }
   │
   ▼
   AI Orchestration Layer processes
   │
   ├─→ Interview Agent processes message
   ├─→ Stream response chunks via WebSocket
   │
   ▼
   Backend: Stream chunks to client
   ws.send({ type: 'agent_message_chunk', content: 'Great!', ... })
   ws.send({ type: 'agent_message_chunk', content: ' What company?', ... })
   ws.send({ type: 'agent_message_complete', ... })
   │
   ▼
   Backend: Update preview
   ws.send({ 
     type: 'preview_update', 
     job_post: { title: 'Software Engineer', ... }
   })
   │
   ▼
   Frontend: Receives and updates
   ├─→ Chat UI: Display streaming message
   └─→ Preview Panel: Update live preview

3. INTERVIEW COMPLETE
   │
   Backend: Detects completion
   │
   ├─→ Post Composer Agent generates post
   │   └─→ Stream generation progress
   │
   ├─→ Formatter Agent polishes post
   │   └─→ Stream formatting updates
   │
   ▼
   Backend: Send complete post
   ws.send({
     type: 'post_complete',
     job_post: { full post data },
     is_complete: true
   })
   │
   ▼
   Frontend: Display complete post
   ├─→ Show all sections
   └─→ Enable save/copy buttons

4. REAL-TIME UPDATES
   │
   Backend: Any state change
   │
   ├─→ Preview update → ws.send({ type: 'preview_update', ... })
   ├─→ Section regenerated → ws.send({ type: 'section_updated', ... })
   └─→ Error occurred → ws.send({ type: 'error', message: '...' })
   │
   ▼
   Frontend: Instantly updates UI
```

### WebSocket Message Types

```
CLIENT → SERVER:
  {
    type: 'user_message',
    content: string,
    session_id: string
  }
  
  {
    type: 'regenerate_section',
    section_type: string,
    session_id: string
  }
  
  {
    type: 'ping',
    timestamp: number
  }

SERVER → CLIENT:
  {
    type: 'connected',
    session_id: string,
    initial_question: string
  }
  
  {
    type: 'typing',
    status: boolean
  }
  
  {
    type: 'agent_message_chunk',
    content: string,
    is_complete: boolean
  }
  
  {
    type: 'agent_message_complete',
    full_message: string
  }
  
  {
    type: 'preview_update',
    job_post: object,
    is_complete: boolean
  }
  
  {
    type: 'post_complete',
    job_post: object
  }
  
  {
    type: 'section_updated',
    section_type: string,
    content: any
  }
  
  {
    type: 'error',
    message: string,
    code: string
  }
  
  {
    type: 'pong',
    timestamp: number
  }
```

### Data Flow (WebSocket-Based)

```
User sends message via WebSocket
    │
    ▼
WebSocket Handler receives message
    │
    ▼
Store message in database
    │
    ▼
Send typing indicator to client
    │
    ▼
AI Orchestration Layer triggered
    │
    ▼
Interview Agent processes message
    │
    ├─→ Stream response chunks via WebSocket
    ├─→ Extracts job information
    ├─→ Determines if complete
    └─→ Generates next question
    │
    ▼
If interview complete:
    │
    ├─→ Post Composer Agent generates post
    │   │
    │   └─→ Stream generation progress
    │   │
    │   └─→ Formatter Agent polishes post
    │       │
    │       └─→ Stream formatting updates
    │
    ▼
Backend stores:
    ├─→ Message in database
    ├─→ Updated session state
    └─→ Job post (if complete)
    │
    ▼
WebSocket broadcasts updates:
    ├─→ Agent response (streamed)
    ├─→ Preview update (real-time)
    └─→ Completion status
    │
    ▼
Frontend receives via WebSocket:
    ├─→ Chat UI updates with streaming message
    └─→ Live Preview updates instantly
```

---

## 🚀 PHASE 2 — Agent Prompts (Full Professional Prompts)

### 1) Interview Agent Prompt

**Role:** Professional HR Assistant conducting structured interviews

**Core Behavior:**
- Acts as an experienced HR professional with expertise in job post creation
- Asks **ONE question at a time** - never multiple questions together
- Waits for complete answer before proceeding
- Follows a logical, structured interview flow
- Adapts tone dynamically based on job type and seniority level

**Required Data Collection:**
1. **Job Title** (essential - start here)
2. **Company** (organization name)
3. **Summary** (brief overview of the role)
4. **Responsibilities** (5-7 key responsibilities)
5. **Requirements** (qualifications, experience, must-haves)
6. **Skills** (technical and soft skills - 8-12 total)
7. **Work Type** (onsite / hybrid / remote)
8. **Location** (city, country, or "remote")
9. **Seniority Level** (entry, mid, senior, lead, executive)
10. **Salary** (optional - if appropriate to ask)
11. **Extra Perks** (benefits, culture, growth opportunities)

**Interview Flow:**
```
1. Job Title & Company → "What position are you looking to fill?"
2. Location & Work Arrangement → "Is this role remote, hybrid, or on-site?"
3. Job Type → "Is this a full-time, part-time, or contract position?"
4. Seniority Level → "What level is this role - entry, mid, senior, or executive?"
5. Key Responsibilities → "What are the main responsibilities for this role?"
6. Requirements → "What qualifications and experience are required?"
7. Required Skills → "What skills are essential for this position?"
8. Preferred Skills → "Are there any nice-to-have skills?"
9. Company Culture → "What makes your company culture unique?"
10. Compensation → "Would you like to include salary range or benefits info?"
```

**Completion Detection:**
- Stops asking **only when** all essential data is collected:
  - ✓ Job Title
  - ✓ At least 3-5 Responsibilities
  - ✓ Requirements
  - ✓ Required Skills (at least 3-5)
  - ✓ Job Type and Seniority Level
- When complete, signals: `[INTERVIEW_COMPLETE]`
- **Never writes the post** until interview is complete

**Tone Adaptation:**
- **Executive/C-Suite:** Formal, strategic, results-oriented
- **Tech Roles:** Modern, innovative, problem-solving focused
- **Entry-Level:** Friendly, encouraging, growth-oriented
- **Senior Roles:** Professional, impact-focused, leadership emphasis

**System Prompt:**
```
You are an expert HR hiring assistant with years of experience in recruiting and job post creation. Your role is to conduct a structured, professional interview with an HR/Recruiter to gather comprehensive information about a job position.

CORE PRINCIPLES:
1. Ask ONLY ONE question at a time - never ask multiple questions in a single response
2. Wait for the user's complete answer before proceeding
3. Be conversational, friendly, and professional - make the HR feel comfortable
4. Follow a logical, structured interview flow
5. Adapt your tone based on the job type and seniority level
6. Ask clarifying questions if information is vague or incomplete
7. Do NOT generate the job post - your only job is to collect information
8. When you have sufficient information, clearly indicate the interview is complete

When complete, end your response with: [INTERVIEW_COMPLETE]
```

---

### 2) Post Composer Agent Prompt

**Role:** Convert structured HR answers into complete LinkedIn-style hiring post

**Core Behaviors:**
- Generate clean, powerful job title
- Create short, attractive intro paragraph (2-4 sentences)
- Format responsibilities as bullet points starting with strong action verbs
- Create requirements list (4-6 items)
- Generate skills list (8-12 items)
- Generate keywords optimized for LinkedIn search (5-10 keywords)
- Generate relevant hashtags (5-8 hashtags, mix of general and specific)
- Use clean, professional English
- Adapt tone based on job type
- Structure output for UI section display

**Output Structure:**
```json
{
  "title": "Job Title",
  "summary": "2-4 sentence compelling summary",
  "responsibilities": [
    "Action verb + responsibility 1",
    "Action verb + responsibility 2",
    ...
  ],
  "requirements": [
    "Requirement 1",
    "Requirement 2",
    ...
  ],
  "skills": [
    "Skill 1",
    "Skill 2",
    ...
  ],
  "keywords": [
    "keyword 1",
    "keyword 2",
    ...
  ],
  "hashtags": [
    "hashtag1",
    "hashtag2",
    ...
  ],
  "tone_type": "professional/tech/casual/executive"
}
```

**System Prompt:**
```
You are an expert LinkedIn hiring post writer with a proven track record of creating engaging, high-performing job posts that attract top talent.

LINKEDIN POST BEST PRACTICES:
1. Hook the reader in the first 1-2 sentences
2. Use strong, action-oriented language
3. Highlight impact and growth opportunities
4. Be specific about responsibilities and requirements
5. Show company culture and values
6. Use bullet points for easy scanning
7. Include a clear call-to-action
8. Optimize for LinkedIn's algorithm with relevant keywords
9. Keep it professional but approachable
10. Avoid jargon unless it's industry-standard

CONTENT REQUIREMENTS:
- Summary: 2-4 sentences that hook the reader and highlight the opportunity
- Responsibilities: 5-7 clear, action-oriented bullet points starting with strong verbs
- Requirements: 4-6 specific qualifications, experience levels, and must-have skills
- Skills: Mix of technical and soft skills (8-12 total)
- Keywords: 5-10 LinkedIn-optimized keywords for search visibility
- Hashtags: 5-8 relevant hashtags (mix of general and specific, without # symbol)

TONE ADAPTATION:
- Executive: Confident, strategic, results-oriented
- Tech: Modern, innovative, problem-solving focused
- Entry-Level: Welcoming, growth-oriented, learning-focused
- Senior: Experienced, knowledgeable, growth-focused
```

---

### 3) Formatter Agent Prompt

**Purpose:** Polish the generated post to publication-ready quality

**Core Behaviors:**
- Improve grammar and spelling
- Improve structure and flow
- Create perfectly formatted bullet points
- Add appropriate line breaks and spacing
- Remove repeated or redundant content
- Ensure it looks identical to real LinkedIn hiring posts
- No emojis unless explicitly requested
- Make the post easy to read and scan

**Formatting Rules:**
1. **Bullet Points:**
   - Start each bullet with a strong action verb
   - Keep bullets concise (one clear idea per bullet)
   - Use parallel structure (same grammatical form)
   - Remove redundant or repetitive bullets
   - Aim for 5-7 responsibilities, 4-6 requirements

2. **Language & Tone:**
   - Use clean, professional English
   - Remove fluff, filler words, and unnecessary phrases
   - Eliminate repetitive phrases or ideas
   - Ensure consistent tone throughout
   - Use active voice (preferred) over passive voice
   - Keep sentences clear and concise

3. **Spacing & Structure:**
   - Add appropriate spacing between sections
   - Ensure proper paragraph breaks
   - Make content scannable and easy to read
   - Use consistent formatting throughout

4. **LinkedIn Optimization:**
   - Format like real LinkedIn HR posts from top companies
   - Ensure hashtags are properly formatted (without # in the array)
   - Make keywords natural and relevant
   - Keep the post engaging, not robotic

5. **Quality Checks:**
   - No typos or grammatical errors
   - No awkward phrasing
   - No repetitive content
   - Professional but approachable
   - Clear and actionable

**System Prompt:**
```
You are an expert content editor and formatter specializing in LinkedIn hiring posts. Your expertise ensures every post is polished, professional, and ready for publication.

Your goal is to make the post polished, professional, and LinkedIn-ready while maintaining the original intent and information.

Format the post to look identical to real LinkedIn hiring posts from professional companies.
```

---

## 🚀 PHASE 3 — Database Flow Diagram

### Database Schema

```
┌─────────────────────────────────────────────────────────────┐
│                      DATABASE STRUCTURE                       │
└─────────────────────────────────────────────────────────────┘

┌──────────────┐
│    users     │
├──────────────┤
│ id (PK)      │
│ email        │──┐
│ password     │  │
│ name         │  │
│ company      │  │
│ role         │  │
│ created_at   │  │
└──────────────┘  │
                  │
                  │ (1) ──→ (many)
                  │
┌─────────────────┴──────────┐
│                            │
│  ┌──────────────┐  ┌──────────────┐
│  │   sessions   │  │  job_posts   │
│  ├──────────────┤  ├──────────────┤
│  │ id (PK)      │  │ id (PK)      │
│  │ user_id (FK) │◄─┤ user_id (FK) │
│  │ session_id   │  │ title        │
│  │ is_complete  │  │ summary      │
│  │ created_at   │  │ responsib... │
│  └──────┬───────┘  │ requirements │
│         │          │ skills       │
│         │ (1)      │ keywords     │
│         │          │ hashtags    │
│         │ (many)   │ tone_type   │
│         │          │ created_at  │
│         │          │ updated_at  │
│         │          └──────────────┘
│         │
│  ┌──────▼───────┐
│  │   messages   │
│  ├──────────────┤
│  │ id (PK)      │
│  │ session_id   │
│  │   (FK)       │
│  │ sender       │
│  │   (user/     │
│  │    agent)    │
│  │ content      │
│  │ created_at   │
│  └──────────────┘
│
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    DATABASE FLOW                             │
└─────────────────────────────────────────────────────────────┘

1. USER STARTS SESSION
   │
   ├─→ INSERT INTO sessions (user_id, session_id, is_complete)
   │   └─→ Returns: session_id
   │
   └─→ Session record created

2. USER SENDS MESSAGE
   │
   ├─→ INSERT INTO messages (session_id, sender='user', content)
   │   └─→ Message stored with session reference
   │
   └─→ Agent processes and responds

3. AGENT RESPONDS
   │
   ├─→ INSERT INTO messages (session_id, sender='agent', content)
   │   └─→ Agent message stored
   │
   └─→ UPDATE sessions SET job_info = {...}

4. INTERVIEW COMPLETE
   │
   ├─→ INSERT INTO job_posts (
   │       user_id, title, summary, responsibilities,
   │       requirements, skills, keywords, hashtags
   │     )
   │   └─→ Job post created
   │
   ├─→ UPDATE sessions SET is_complete = true, job_post_id = {id}
   │   └─→ Session linked to job post
   │
   └─→ User can now retrieve post

5. USER RETRIEVES POSTS
   │
   ├─→ SELECT * FROM job_posts WHERE user_id = {user_id}
   │   └─→ Returns all user's posts
   │
   └─→ Displayed in Dashboard

6. USER EDITS POST
   │
   ├─→ UPDATE job_posts SET 
   │       title = {...}, summary = {...}, ...
   │   WHERE id = {post_id}
   │   └─→ Post updated
   │
   └─→ Changes saved
```

### Relationships

```
users (1) ────────────────→ (many) job_posts
  │                              │
  │                              │
  │ (1) ───────────────────────→ (many) sessions
  │                                    │
  │                                    │
  │                                    │ (1) ──→ (many) messages
  │                                    │
  │                                    │
  └───────────────────────────────────┘
         sessions (1) ──→ (1) job_posts (when complete)
```

---

## 🚀 PHASE 4 — Complete Task List for Developer Team

### Module 1 — Frontend (Next.js)

#### Chat UI
- [ ] Build chat message display component
- [ ] Implement message bubbles (user/agent styling)
- [ ] Add message input field with send button
- [ ] Implement typing indicator for agent responses
- [ ] Add scroll-to-bottom on new messages
- [ ] Implement message timestamps
- [ ] Add message loading states
- [ ] Handle message errors gracefully

#### Streaming Responses
- [ ] Integrate Server-Sent Events (SSE) or WebSocket
- [ ] Implement streaming message display
- [ ] Add real-time typing indicators
- [ ] Handle connection errors and reconnection
- [ ] Optimize for performance with large conversations

#### Live Post Preview Panel
- [ ] Build preview component structure
- [ ] Implement section-by-section display:
  - [ ] Title section
  - [ ] Summary section
  - [ ] Responsibilities list
  - [ ] Requirements list
  - [ ] Skills tags
  - [ ] Keywords display
  - [ ] Hashtags display
- [ ] Add real-time update mechanism
- [ ] Implement section regeneration buttons
- [ ] Add "Save Post" button
- [ ] Add "Copy to Clipboard" functionality
- [ ] Style to match LinkedIn post appearance

#### Dashboard Page
- [ ] Create dashboard layout
- [ ] Build post list/grid view
- [ ] Implement post cards with preview
- [ ] Add post filtering and sorting
- [ ] Add pagination for large lists
- [ ] Implement search functionality
- [ ] Add empty state when no posts

#### Saved Posts Page
- [ ] Create saved posts view
- [ ] Implement full post display
- [ ] Add edit functionality
- [ ] Add delete confirmation
- [ ] Implement post duplication
- [ ] Add export options (PDF, text)

#### Copy-to-Clipboard Feature
- [ ] Implement clipboard API integration
- [ ] Format post for copying (plain text)
- [ ] Add success/error notifications
- [ ] Support multiple formats (LinkedIn, plain text)

#### Authentication Pages
- [ ] Build login page
- [ ] Build signup page
- [ ] Implement JWT token storage
- [ ] Add password reset flow
- [ ] Implement protected routes
- [ ] Add session management
- [ ] Handle authentication errors

#### Settings Page
- [ ] Create settings layout
- [ ] Add tone preference selector
- [ ] Add template options
- [ ] Implement user profile editing
- [ ] Add notification preferences
- [ ] Save settings to backend

---

### Module 2 — Backend (FastAPI)

#### Authentication (JWT)
- [ ] Implement user registration endpoint
- [ ] Implement user login endpoint
- [ ] Create JWT token generation
- [ ] Add token validation middleware
- [ ] Implement password hashing (bcrypt)
- [ ] Add refresh token mechanism
- [ ] Create user profile endpoints
- [ ] Add password reset functionality

#### Chat Endpoints
- [ ] Build `/api/start-chat` endpoint
  - [ ] Create new session
  - [ ] Initialize AI orchestrator
  - [ ] Return initial question
- [ ] Build `/api/send-message` endpoint
  - [ ] Validate session
  - [ ] Store user message
  - [ ] Process through AI
  - [ ] Store agent response
  - [ ] Return updated preview
- [ ] Build `/api/post-preview/{session_id}` endpoint
  - [ ] Retrieve current post state
  - [ ] Return formatted preview

#### AI Orchestration Layer
- [ ] Create orchestrator class
- [ ] Implement session state management
- [ ] Coordinate agent execution flow
- [ ] Handle agent errors gracefully
- [ ] Implement conversation memory
- [ ] Add completion detection logic
- [ ] Optimize for performance

#### Post Generation Pipeline
- [ ] Integrate Interview Agent
- [ ] Integrate Composer Agent
- [ ] Integrate Formatter Agent
- [ ] Implement agent chaining
- [ ] Add error handling between agents
- [ ] Implement retry logic
- [ ] Add logging for debugging

#### Post Management Endpoints
- [ ] Build `/api/save-post` endpoint
  - [ ] Validate session
  - [ ] Create job_post record
  - [ ] Link to user
  - [ ] Return saved post
- [ ] Build `/api/posts` endpoint
  - [ ] Filter by user
  - [ ] Add pagination
  - [ ] Add sorting options
  - [ ] Return formatted list
- [ ] Build `/api/posts/{id}` endpoint
  - [ ] Get single post
  - [ ] Validate ownership
- [ ] Build `/api/posts/{id}` PUT endpoint
  - [ ] Update post
  - [ ] Validate ownership
- [ ] Build `/api/posts/{id}` DELETE endpoint
  - [ ] Delete post
  - [ ] Validate ownership

#### Session Tracking
- [ ] Implement session storage
- [ ] Add session expiration
- [ ] Track session activity
- [ ] Implement session cleanup
- [ ] Add session analytics

#### Logging
- [ ] Set up logging framework
- [ ] Log all API requests
- [ ] Log AI agent interactions
- [ ] Log errors with context
- [ ] Implement log rotation
- [ ] Add performance metrics

---

### Module 3 — AI Layer

#### Interview Agent Logic
- [ ] Create Interview Agent class
- [ ] Implement question generation
- [ ] Add completion detection
- [ ] Implement information extraction
- [ ] Add tone adaptation logic
- [ ] Handle edge cases
- [ ] Optimize prompt engineering

#### Composer Agent Logic
- [ ] Create Composer Agent class
- [ ] Implement post generation
- [ ] Add section-by-section creation
- [ ] Implement tone adaptation
- [ ] Add keyword generation
- [ ] Add hashtag generation
- [ ] Optimize for LinkedIn format

#### Formatter Agent Logic
- [ ] Create Formatter Agent class
- [ ] Implement grammar checking
- [ ] Add structure optimization
- [ ] Implement bullet point formatting
- [ ] Add spacing optimization
- [ ] Remove redundant content
- [ ] Polish final output

#### Memory Object
- [ ] Create conversation memory structure
- [ ] Implement memory persistence
- [ ] Add memory retrieval
- [ ] Optimize memory size
- [ ] Implement memory cleanup

#### Required Data Fields
- [ ] Define job_title field
- [ ] Define company field
- [ ] Define responsibilities array
- [ ] Define requirements array
- [ ] Define skills array
- [ ] Define optional fields
- [ ] Create validation schema

#### Job Completeness Logic
- [ ] Define completion criteria
- [ ] Implement completeness check
- [ ] Add missing field detection
- [ ] Create completion scoring
- [ ] Handle partial completion

#### Dynamic Tone System
- [ ] Create tone detection logic
- [ ] Implement tone adaptation
- [ ] Add tone templates
- [ ] Test tone variations
- [ ] Optimize tone selection

#### Templates System
- [ ] Create template structure
- [ ] Implement template selection
- [ ] Add custom templates
- [ ] Test template variations
- [ ] Allow user customization

---

### Module 4 — Database

#### Schema Creation
- [ ] Create users table schema
- [ ] Create sessions table schema
- [ ] Create job_posts table schema
- [ ] Create messages table schema
- [ ] Define all field types
- [ ] Set up constraints
- [ ] Add default values

#### Migrations
- [ ] Set up Alembic
- [ ] Create initial migration
- [ ] Create migration for indexes
- [ ] Create migration for relationships
- [ ] Test migration rollback
- [ ] Document migration process

#### Indexes
- [ ] Add index on users.email
- [ ] Add index on sessions.session_id
- [ ] Add index on sessions.user_id
- [ ] Add index on job_posts.user_id
- [ ] Add index on messages.session_id
- [ ] Add composite indexes where needed
- [ ] Optimize query performance

#### Relationships
- [ ] Set up users → job_posts (1:many)
- [ ] Set up users → sessions (1:many)
- [ ] Set up sessions → messages (1:many)
- [ ] Set up sessions → job_posts (1:1, optional)
- [ ] Add foreign key constraints
- [ ] Set up cascade deletes
- [ ] Test relationship integrity

#### CRUD Operations
- [ ] Test user creation
- [ ] Test session creation
- [ ] Test message creation
- [ ] Test job_post creation
- [ ] Test update operations
- [ ] Test delete operations
- [ ] Test query performance

#### Search Optimization
- [ ] Implement full-text search
- [ ] Add search indexes
- [ ] Optimize search queries
- [ ] Test search performance
- [ ] Add search ranking

---

### Module 5 — QA & Deployment

#### Debugging
- [ ] Debug message flow end-to-end
- [ ] Test session persistence
- [ ] Verify AI agent responses
- [ ] Check database transactions
- [ ] Test error handling
- [ ] Verify authentication flow

#### Testing
- [ ] Test Interview Agent accuracy
- [ ] Validate post formatting quality
- [ ] Test all API endpoints
- [ ] Test frontend components
- [ ] Test user flows
- [ ] Performance testing
- [ ] Load testing

#### Deployment - Backend
- [ ] Set up production server
- [ ] Configure environment variables
- [ ] Set up database connection
- [ ] Deploy FastAPI application
- [ ] Set up process manager (PM2/supervisor)
- [ ] Configure logging
- [ ] Set up monitoring

#### Deployment - Frontend
- [ ] Build production bundle
- [ ] Set up hosting (Vercel/Netlify)
- [ ] Configure environment variables
- [ ] Set up CDN
- [ ] Optimize assets
- [ ] Test production build

#### SSL Setup
- [ ] Obtain SSL certificates
- [ ] Configure HTTPS
- [ ] Set up certificate renewal
- [ ] Test SSL configuration

#### Monitoring
- [ ] Set up error tracking (Sentry)
- [ ] Set up performance monitoring
- [ ] Configure uptime monitoring
- [ ] Set up log aggregation
- [ ] Create alerting rules
- [ ] Set up analytics

---

## 🚀 PHASE 5 — User Flow Map

```
┌─────────────────────────────────────────────────────────────┐
│                      USER FLOW DIAGRAM                       │
└─────────────────────────────────────────────────────────────┘

START
  │
  ▼
┌─────────────────┐
│  User Logs In   │
│  (Email/Pass)   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│  Dashboard / Home Page  │
│  - View saved posts      │
│  - Create new post      │
└────────┬─────────────────┘
         │
         │ User clicks "Create New Job Post"
         │
         ▼
┌─────────────────────────┐
│  Chat Session Starts     │
│  - Session ID created   │
│  - AI initialized       │
└────────┬─────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Interview Agent         │
│  Asks First Question    │
│  "What position are     │
│   you looking to fill?" │
└────────┬─────────────────┘
         │
         ▼
┌─────────────────────────┐
│  User Answers           │
│  - Message sent to API  │
│  - Stored in database   │
└────────┬─────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Live Preview Updates   │
│  - Shows extracted info │
│  - Updates in real-time │
└────────┬─────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Agent Continues        │
│  Asking Questions       │
│  - One at a time        │
│  - Follows flow         │
└────────┬─────────────────┘
         │
         │ Loop continues until...
         │
         ▼
┌─────────────────────────┐
│  All Data Collected?    │
│  - Job title ✓          │
│  - Responsibilities ✓   │
│  - Requirements ✓       │
│  - Skills ✓             │
└────────┬─────────────────┘
         │
         │ Yes
         │
         ▼
┌─────────────────────────┐
│  Interview Complete     │
│  [INTERVIEW_COMPLETE]   │
└────────┬─────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Composer Agent         │
│  Generates Full Post    │
│  - Title                │
│  - Summary              │
│  - All sections         │
└────────┬─────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Formatter Agent        │
│  Polishes Post          │
│  - Grammar              │
│  - Structure            │
│  - Formatting           │
└────────┬─────────────────┘
         │
         ▼
┌─────────────────────────┐
│  User Reviews Post      │
│  - Sees full preview    │
│  - Can regenerate       │
│  - Can edit sections    │
└────────┬─────────────────┘
         │
         │ User clicks "Save Post"
         │
         ▼
┌─────────────────────────┐
│  Post Saved to Database │
│  - Linked to user       │
│  - Stored permanently   │
└────────┬─────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Post Appears in        │
│  Dashboard              │
│  - In saved posts list  │
│  - With metadata        │
└────────┬─────────────────┘
         │
         ▼
┌─────────────────────────┐
│  User Can:              │
│  - View full post       │
│  - Copy to clipboard   │
│  - Edit post            │
│  - Regenerate sections  │
│  - Delete post          │
└────────┬─────────────────┘
         │
         ▼
      END / LOOP BACK
```

### Alternative Flows

```
REGENERATE SECTION FLOW:
  User clicks "Regenerate" on section
    │
    ▼
  API call to /regenerate-section
    │
    ▼
  Formatter Agent regenerates section
    │
    ▼
  Updated section displayed
    │
    ▼
  User can save or continue editing

EDIT POST FLOW:
  User clicks "Edit" on saved post
    │
    ▼
  Post loaded into editor
    │
    ▼
  User makes changes
    │
    ▼
  Changes saved to database
    │
    ▼
  Updated post displayed
```

---

## 🚀 PHASE 6 — UI/UX Wireframe Structure

### 1) Chat + Live Preview Screen (Main Workspace)

```
┌─────────────────────────────────────────────────────────────────┐
│  HR Hiring Assistant                    [View Dashboard] [User]  │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────────┐  ┌──────────────────────────┐   │
│  │   CHAT PANEL (Left)       │  │  LIVE PREVIEW (Right)     │   │
│  ├──────────────────────────┤  ├──────────────────────────┤   │
│  │                           │  │  Live Preview             │   │
│  │  AI Hiring Assistant      │  │  Your LinkedIn post      │   │
│  │  Ask me about your job    │  │  [Complete] badge        │   │
│  ├──────────────────────────┤  ├──────────────────────────┤   │
│  │                           │  │                          │   │
│  │  🤖 Hi! I'm here to help  │  │  ┌────────────────────┐  │   │
│  │     you create a         │  │  │ Job Title          │  │   │
│  │     professional          │  │  │                    │  │   │
│  │     LinkedIn hiring post. │  │  │                    │  │   │
│  │     What position are     │  │  └────────────────────┘  │   │
│  │     you looking to fill?  │  │                          │   │
│  │                           │  │  Summary:               │   │
│  │  ────────────────────────│  │  [Regenerate]          │   │
│  │                           │  │  [Text content...]     │   │
│  │  👤 Software Engineer     │  │                          │   │
│  │                           │  │  Responsibilities:      │   │
│  │  ────────────────────────│  │  [Regenerate]          │   │
│  │                           │  │  • Bullet point 1      │   │
│  │  🤖 Great! What company?  │  │  • Bullet point 2      │   │
│  │                           │  │  • Bullet point 3      │   │
│  │  ────────────────────────│  │                          │   │
│  │                           │  │  Requirements:         │   │
│  │  👤 TechCorp Inc.         │  │  [Regenerate]          │   │
│  │                           │  │  • Requirement 1       │   │
│  │  ────────────────────────│  │  • Requirement 2       │   │
│  │                           │  │                          │   │
│  │  🤖 [Typing...]          │  │  Skills:                │   │
│  │     ● ● ●                │  │  [Regenerate]          │   │
│  │                           │  │  [Tag] [Tag] [Tag]     │   │
│  │                           │  │                          │   │
│  │                           │  │  Keywords:             │   │
│  │                           │  │  keyword1, keyword2   │   │
│  │                           │  │                          │   │
│  │                           │  │  #hashtag1 #hashtag2   │   │
│  │                           │  │                          │   │
│  │                           │  │  [Save Post] [Copy]     │   │
│  │                           │  │  [Apply Now]           │   │
│  ├──────────────────────────┤  ├──────────────────────────┤   │
│  │  [Type your answer...]  │  │                          │   │
│  │  [Send]                  │  │                          │   │
│  └──────────────────────────┘  └──────────────────────────┘   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### 2) Dashboard

```
┌─────────────────────────────────────────────────────────────────┐
│  Saved Hiring Posts                    [Create New] [Settings]   │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Post Card   │  │  Post Card   │  │  Post Card   │          │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤          │
│  │ Software      │  │ Product      │  │ Marketing    │          │
│  │ Engineer      │  │ Manager      │  │ Specialist   │          │
│  │               │  │              │  │              │          │
│  │ We're looking│  │ Join our...  │  │ Seeking a... │          │
│  │ for a...     │  │              │  │              │          │
│  │               │  │              │  │              │          │
│  │ Created:     │  │ Created:     │  │ Created:     │          │
│  │ Jan 15, 2024 │  │ Jan 10, 2024 │  │ Jan 5, 2024  │          │
│  │               │  │              │  │              │          │
│  │ [View] [Copy]│  │ [View] [Copy]│  │ [View] [Copy]│          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Post Card   │  │  Post Card   │  │  Post Card   │          │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤          │
│  │ Data Analyst │  │ UX Designer  │  │ DevOps Eng   │          │
│  │ ...          │  │ ...          │  │ ...          │          │
│  │ [View] [Copy]│  │ [View] [Copy]│  │ [View] [Copy]│          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                   │
│  [< Previous]  [1] [2] [3] [Next >]                             │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### 3) Login Page

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                   │
│                                                                   │
│                    ┌─────────────────────┐                      │
│                    │                     │                      │
│                    │   HR Hiring         │                      │
│                    │   Assistant         │                      │
│                    │                     │                      │
│                    └─────────────────────┘                      │
│                                                                   │
│                    ┌─────────────────────┐                      │
│                    │  Email              │                      │
│                    │  [________________] │                      │
│                    └─────────────────────┘                      │
│                                                                   │
│                    ┌─────────────────────┐                      │
│                    │  Password           │                      │
│                    │  [________________] │                      │
│                    └─────────────────────┘                      │
│                                                                   │
│                    ┌─────────────────────┐                      │
│                    │    [Continue]       │                      │
│                    └─────────────────────┘                      │
│                                                                   │
│                    [Forgot Password?]                            │
│                    [Don't have an account? Sign up]             │
│                                                                   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### 4) Saved Post View (Modal/Page)

```
┌─────────────────────────────────────────────────────────────────┐
│  Software Engineer - TechCorp Inc.                    [× Close] │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                                                          │   │
│  │  Software Engineer                                       │   │
│  │                                                          │   │
│  │  Summary:                                                │   │
│  │  [Regenerate]                                            │   │
│  │  We're looking for a talented Software Engineer to join │   │
│  │  our growing team. You'll work on cutting-edge projects │   │
│  │  and have the opportunity to make a real impact.        │   │
│  │                                                          │   │
│  │  Responsibilities:                                       │   │
│  │  [Regenerate]                                            │   │
│  │  • Design and develop scalable software solutions        │   │
│  │  • Collaborate with cross-functional teams              │   │
│  │  • Write clean, maintainable code                       │   │
│  │  • Participate in code reviews                          │   │
│  │                                                          │   │
│  │  Requirements:                                           │   │
│  │  [Regenerate]                                            │   │
│  │  • 3+ years of software development experience          │   │
│  │  • Strong knowledge of Python/JavaScript                │   │
│  │  • Experience with cloud platforms                      │   │
│  │                                                          │   │
│  │  Skills:                                                 │   │
│  │  [Regenerate]                                            │   │
│  │  [Python] [JavaScript] [AWS] [Docker] [Git]            │   │
│  │                                                          │   │
│  │  #hiring #softwareengineer #techjobs #remotework        │   │
│  │                                                          │   │
│  │  ┌──────────────────────────────────────────────────┐   │   │
│  │  │ [Copy to Clipboard]  [Edit]  [Delete]            │   │   │
│  │  └──────────────────────────────────────────────────┘   │   │
│  │                                                          │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Summary

This document provides a complete overview of:

1. **System Architecture** - How all components connect and interact
2. **Agent Prompts** - Detailed specifications for all three AI agents
3. **Database Flow** - Schema, relationships, and data flow
4. **Development Tasks** - Complete checklist for the development team
5. **User Flow** - Step-by-step user journey through the application
6. **UI/UX Wireframes** - Visual structure of all main screens

This documentation serves as a comprehensive guide for developers, designers, and stakeholders to understand and build the HR Hiring Assistant system.

---

## 📊 Implementation Status

**See `IMPLEMENTATION_STATUS.md` for detailed implementation verification.**

### Quick Status:
- ✅ **Phase 2** - Agent Prompts: Fully implemented
- ✅ **Phase 3** - Database Flow: Fully implemented  
- ✅ **Phase 5** - User Flow: Mostly implemented
- ✅ **Phase 6** - UI/UX Wireframes: Fully implemented
- ⚠️ **Phase 1** - Architecture: Partially implemented (REST API instead of WebSocket)
- 📋 **Phase 4** - Task List: Documentation/checklist (ongoing)

**Note:** The current implementation uses REST API instead of WebSocket as documented in Phase 1. WebSocket support needs to be added to match the architecture.

