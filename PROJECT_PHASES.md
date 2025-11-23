# HR Hiring Assistant — Project Phases

## 🔵 Phase 1 — Project Definition

### Core Concept

A simple HR platform where the user (HR/Recruiter) chats with an AI hiring agent.

- The agent asks structured questions about the job
- HR answers naturally
- A live, LinkedIn-style Hiring Post Preview is generated on the right side of the screen

**Final Result**: A professional, polished hiring post ready for LinkedIn.

---

## 🔵 Phase 2 — UX Structure

### Main Page: Chat Builder

Two side-by-side sections:

#### 1) Left Panel — AI Chat

- HR chats with the AI agent
- Agent asks questions one by one
- HR answers normally
- The conversation becomes the source of all job details

#### 2) Right Panel — Live Hiring Post Preview

Updates instantly with every answer:

- Job Title
- Intro paragraph
- Responsibilities (bullet points)
- Requirements
- Skills
- Keywords for LinkedIn
- Hashtags
- CTA (Apply now)

**Everything updates live while chatting.**

---

## 🔵 Phase 3 — AI Logic Design (High-Level)

Three AI agents working together:

### A) Interview Agent

- Asks the right questions
- Controls the flow
- One question at a time
- Stops only when it has all job information

### B) Post Composer Agent

After the Interview Agent finishes:

- Builds the full hiring post
- Creates job summary
- Generates responsibilities
- Generates requirements
- Generates skills
- Generates LinkedIn keywords
- Generates hashtags
- Writes with the right tone based on job type & seniority

### C) Formatter Agent

Polishes everything:

- Bullet points
- Spacing
- Paragraph formatting
- Clean English
- Professional tone
- No fluff

---

## 🔵 Phase 4 — Data Model

### JobPost

```
- id
- title
- summary
- responsibilities[]
- requirements[]
- skills[]
- keywords[]
- hashtags[]
- tone_type
- created_at
- updated_at
- user_id
```

### User

```
- id
- email
- password
- name
- company
- role
```

---

## 🔵 Phase 5 — Backend Structure (FastAPI)

### Endpoints

#### `POST /start-chat`
Starts a new job creation session

#### `POST /send-message`
HR sends message → AI replies → returns updated preview

#### `GET /post-preview/{session_id}`
Returns the current live-generated post

#### `POST /save-post`
Saves the post to the dashboard

#### `GET /posts`
Shows saved posts for the user

#### `POST /regenerate-section`
Regenerates any section:

- Responsibilities
- Skills
- Summary
- Hashtags
- Keywords

---

## 🔵 Phase 6 — Frontend Structure (React / Next.js)

### 1) Chat Panel

- Clean, minimal UI
- Messages from HR and Agent
- Real-time updates
- Typing indicator
- Scrollable history

### 2) Post Preview Panel

Displays:

- Title
- Summary paragraph
- Responsibilities list
- Requirements list
- Skills
- Keywords
- Hashtags
- CTA

**Everything updates instantly as the HR answers questions.**

### 3) Dashboard

- List of saved hiring posts
- Open and view
- Edit or regenerate
- Copy to clipboard
- Delete

---

## 🔵 Phase 7 — AI Prompt Strategy (High-Level)

### Interview Agent Prompt

- Ask only one question at a time
- Follow a structured interviewing path
- Adjust tone based on the job
- Stop when job details are complete
- Don't generate the post early

### Composer Prompt

- Create a clean LinkedIn-style post
- Use strong, simple, professional English
- Highlight impact, responsibilities, and required skills
- Include hashtags + keywords for reach

### Formatting Prompt

- Add spacing
- Proper bullet points
- Clean English
- Remove repetitive phrases
- Format like real LinkedIn HR posts

---

## 🔵 Phase 8 — Logical Flow

1. HR starts a new chat
2. AI asks question #1
3. HR responds
4. AI updates the next question
5. Live Preview updates
6. After enough details → AI composes the full post
7. Preview becomes complete
8. HR refines, regenerates, or saves
9. HR copies and posts on LinkedIn
10. HR can return to previous saved posts in Dashboard

---

## 🔵 Phase 9 — Versions

### V1 (Launch Version)

- Chat
- Live preview
- Save post
- Dashboard
- Responsibilities
- Skills
- Keywords
- Hashtags
- Basic dynamic tone

### V2 (Advanced)

- Job-based templates
- LinkedIn algorithm optimization
- Automatic seniority detection
- Multi-language support
- Multiple versions (short, long, punchy)
- Team collaboration

---

## 📋 Summary

This HR Hiring Assistant is a **two-panel interface** where:

- **Left side**: HR converses with an AI agent about job requirements
- **Right side**: A live LinkedIn-style hiring post updates in real-time

The project leverages **three specialized AI agents** (Interview, Composer, Formatter) to ensure structured data collection and high-quality post generation, with a **FastAPI backend** and **React/Next.js frontend** for a seamless user experience.
