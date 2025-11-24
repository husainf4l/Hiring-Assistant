# Job Finder Assistant — Project Blueprint

## 🔵 Phase 1 — Project Definition

### Core Concept

A simple job-search assistant where the user (Job Seeker) chats with an AI Job Finder Agent.

The agent asks structured questions to understand the user’s background → the user answers → A live, LinkedIn-style Job Recommendation Panel is generated on the right side of the screen.

**Final Result**: A personalized list of suitable jobs (from your internal job database), displayed live with match scores and explanations.

---

## 🔵 Phase 2 — UX Structure

### Main Page: Job Finder

Two side-by-side sections:

#### 1) Left Panel — AI Chat
- User chats with the Job Finder Agent
- Agent asks questions one by one
- User answers normally
- The conversation becomes the source of the job seeker profile
- Agent dynamically updates the seeker’s preferences

#### 2) Right Panel — Live Job Recommendation Cards
Updates instantly with every answer:
- Job Title
- Company
- Location
- Required Skills
- Match Percentage
- Why This Job Fits You
- Buttons: View / Save / Apply

**Everything updates live while chatting.**

---

## 🔵 Phase 3 — AI Logic Design (High-Level)

Three AI agents working together:

### A) Interview Agent (Job Seeker Profiler)
- Asks the right questions
- Collects user background, skills, experience, location, salary, job titles
- Controls the flow
- One question at a time
- Stops only when the profile is complete

### B) Job Matching Agent
After the Interview Agent finishes:
- Builds the job seeker profile
- Searches your internal job database
- Calculates match score
- Chooses top relevant jobs
- Generates short-fit explanations
- Sends matched jobs to the preview panel

### C) Formatter Agent
Polishes everything:
- Clean job cards
- Clear match percentages
- Skills highlighted
- Professional, simple tone
- No unnecessary text

**Implemented via (Phase 3 scaffold):**
- `backend/job_finder/models.py`
- `backend/job_finder/interview_agent.py`
- `backend/job_finder/matching_agent.py`
- `backend/job_finder/formatter_agent.py`
- `backend/job_finder/orchestrator.py`

---

## 🔵 Phase 4 — Data Model (No Code)

### JobSeekerProfile
- id
- current_role
- skills[]
- years_experience
- preferred_titles[]
- preferred_locations[]
- salary_expectation
- work_type (remote / onsite / hybrid)
- industries[]
- created_at
- updated_at
- user_id

### JobListing
- id
- title
- company
- location
- required_skills[]
- optional_skills[]
- experience_level
- salary_range
- work_type
- description
- created_at

### JobRecommendation
- id
- job_id
- seeker_id
- match_score
- explanation
- created_at

**Implemented via:** `backend/job_finder/db_models.py`

---

## 🔵 Phase 5 — Backend Structure (FastAPI)

### Endpoints
- **POST /api/job-finder/start-chat** — Starts a new job seeker session
- **POST /api/job-finder/send-message** — User sends message → AI replies → job recommendations update
- **GET /api/job-finder/recommendations/{session_id}** — Returns the current live list of job recommendations
- **POST /api/job-finder/save-job** — Saves a job to the user’s dashboard (placeholder)
- **GET /api/job-finder/saved-jobs** — Shows saved jobs for the user (placeholder reuse)
- **POST /api/job-finder/refine-search** — Adjusts filters (remote only, specific skills, new job title, salary range)

**Implemented via:** `backend/job_finder/routes.py`

---

## 🔵 Phase 6 — Frontend Structure (React / Next.js)

### 1) Chat Panel
- Clean UI
- HR-style bubbles
- Agent and user messages
- Typing indicator
- Scrollable history

### 2) Job Recommendation Panel
- Live cards containing:
  - Job Title
  - Company
  - Location
  - Required Skills
  - Match %
  - Explanation
  - View / Save / Apply buttons
- Updates instantly as the user answers questions.

### 3) Dashboard
- Saved jobs
- Match score
- Open job details
- Remove / manage saved jobs

---

## 🔵 Phase 7 — AI Strategy (High-Level)

### Interview Agent Strategy
- Ask one question at a time
- Build a complete profile
- Clarify unclear answers
- Never provide jobs before profile is ready
- **Implemented via:** `backend/job_finder/interview_agent.py`

### Matching Agent Strategy
- Compare user profile with job listings
- Evaluate required vs. optional skills
- Score job titles by similarity
- Consider experience level
- Consider location preference
- Return top matches only
- **Implemented via:** `backend/job_finder/matching_agent.py`

### Formatter Strategy
- Clean card descriptions
- Keep explanations short, helpful, and professional
- No long paragraphs
- Highlight top skills matched
- **Implemented via:** `backend/job_finder/formatter_agent.py`

---

## 🔵 Phase 8 — Logical Flow

1. User starts a new chat
2. Agent asks question #1
3. User responds
4. Agent continues collecting profile
5. When enough data is available → matching begins
6. Job cards on the right update in real-time
7. User can:
   - Save jobs
   - View details
   - Apply
   - Ask for more jobs
   - Filter (remote only, senior roles, etc.)
8. User can return anytime to their Saved Jobs dashboard

**Current Implementation**
- `/api/job-finder/start-chat` → orchestrator session bootstrap
- `/api/job-finder/send-message` → interview loop + matching
- `/job-finder` Next.js page → live chat + job recommendation cards
- `JobFinderOrchestrator` coordinates Interview/Matching/Formatter agents

---

## 🔵 Phase 9 — Versions

### V1 (Launch Version)
- Chat
- Live job recommendation panel
- Save job
- Dashboard
- Basic match score
- Required skill matching
- Basic location preference
- `/job-finder` Next.js page (chat UI + recommendation cards)
- `/api/job-finder/*` backend endpoints and orchestrator pipeline

### V2 (Advanced)
- Multi-language
- CV builder
- Cover letter builder
- Interview preparation
- Skill gap analysis
- Job title prediction
- Career roadmap
- Multiple match algorithms
- Advanced recommendations
- Search filters (salary, company size, industries)


