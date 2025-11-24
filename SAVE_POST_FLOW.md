# Save Post Flow Documentation

## Overview
When a user completes creating a hiring post through the AI conversation, they can save it to their dashboard. This document describes the complete save flow.

## Flow Architecture

### Frontend Flow (User Interface)

1. **Chat Completion**
   - User completes the interview conversation with the AI agent
   - Once all required information is gathered, `isComplete` is set to `true`
   - The "Save Post" button appears in the Preview Panel

2. **Save Button Click**
   - Located in: `frontend/components/PreviewPanel.tsx`
   - When clicked, calls `handleSave()` function
   - Shows "Saving..." state while processing

3. **Save API Call**
   - Calls `savePost(sessionId, userId)` from `frontend/lib/api.ts`
   - Sends POST request to `/api/save-post`
   - Payload: `{ session_id: string, user_id: number }`

4. **Success & Redirect**
   - On successful save, displays success alert
   - Automatically redirects to `/dashboard` after 500ms
   - User sees their saved post in the dashboard grid

### Backend Flow (Server Processing)

1. **Save Post Endpoint**
   - Route: `POST /api/save-post`
   - File: `backend/routes.py` (lines 274-301)
   
2. **Validation**
   - Retrieves chat session from database using `session_id`
   - Verifies `job_post_id` exists in the session
   - Retrieves the job post from database

3. **Save Operation**
   - Updates `user_id` if different from request
   - Returns the saved job post as JSON response

4. **Database Storage**
   - JobPost data is already stored during chat conversation
   - Save endpoint simply associates it with the user

## Database Schema

### JobPost Table
```python
- id: Primary Key
- user_id: User who owns the post
- title: Job title
- summary: Job summary
- company: Company name
- responsibilities: List of responsibilities
- requirements: List of requirements
- skills: Required skills
- keywords: SEO keywords
- hashtags: LinkedIn hashtags
- workplace_type: On-site/Remote/Hybrid
- location: Job location
- job_type: Full-time/Part-time/Contract
- tone_type: Professional/Casual/Formal
- culture_and_team: Company culture description
- compensation_benefits: Compensation details
- call_to_action: CTA message
- created_at: Timestamp
- updated_at: Timestamp
```

## Dashboard Display

### View Saved Posts
- Route: `GET /api/posts?user_id={userId}`
- File: `backend/routes.py` (lines 304-315)
- Returns paginated list of user's saved posts

### Post Card Display
- File: `frontend/app/dashboard/page.tsx`
- Shows:
  - Post title
  - Summary preview (150 characters)
  - Creation date
  - View and Copy buttons

### View Full Post
- Clicking "View" opens a modal
- Displays complete post content
- Allows copying to clipboard

## API Endpoints

### 1. Start Chat Session
```
POST /api/start-chat
Body: { user_id: number }
Response: { session_id, response, is_complete, job_post }
```

### 2. Send Message
```
POST /api/send-message
Body: { session_id, message }
Response: { session_id, response, is_complete, job_post }
```

### 3. Get Post Preview
```
GET /api/post-preview/{session_id}
Response: { session_id, job_post, is_complete }
```

### 4. Save Post (NEW)
```
POST /api/save-post
Body: { session_id, user_id }
Response: { message, job_post }
```

### 5. Get User's Posts
```
GET /api/posts?user_id={userId}&skip=0&limit=100
Response: { posts: JobPost[], total: number }
```

## UI Components

### PreviewPanel.tsx
- Displays live preview of job post being created
- Shows save/copy buttons when `isComplete === true`
- Handles save operation and redirect
- Located: `frontend/components/PreviewPanel.tsx`

### Dashboard Page
- Displays grid of saved posts
- Shows post cards with title, preview, and date
- Modal view for full post details
- Located: `frontend/app/dashboard/page.tsx`

## Styling

### Dashboard Styles (Professional Modern Design)
- Gradient backgrounds (white to light blue)
- Indigo primary color (#6366f1)
- Green accent for AI elements (#10b981)
- Smooth transitions and hover effects
- Cards with elevation on hover
- Located: `frontend/app/globals.css` (lines 733-945)

### Save Button
- Indigo gradient background
- Appears only when chat is complete
- Shows loading state during save
- Located in: `frontend/components/PreviewPanel.tsx` (line 341)

## User Experience Flow

```
1. User clicks "Create New Post" → Chat starts
2. User has conversation with AI → Post data accumulates
3. Chat completes → "Save Post" button appears
4. User clicks "Save Post" → Post saved to database
5. Success notification + Redirect to dashboard
6. Dashboard shows the newly saved post
7. User can view/copy/manage posts from dashboard
```

## Error Handling

- Invalid session: Returns HTTP 404
- No job post in session: Returns HTTP 400
- Database errors: Returns HTTP 500 with error message
- Frontend alerts user of any failures
- User can retry without losing chat history

## Future Enhancements

1. **Authentication**
   - Replace hardcoded user_id (1) with actual user auth
   - Implement JWT or session-based auth

2. **Edit Functionality**
   - Allow users to edit saved posts
   - Add edit button to dashboard cards

3. **Delete Functionality**
   - Add delete button to dashboard
   - Confirm before deletion

4. **Export Options**
   - Export to PDF
   - Export to LinkedIn format
   - Export to email template

5. **Templates**
   - Save as templates
   - Apply templates to new posts

6. **Sharing**
   - Share posts with team
   - Set permissions (view/edit)

## Testing Checklist

- [ ] Start chat creates new session
- [ ] Messages are processed correctly
- [ ] Preview updates in real-time
- [ ] Complete status triggers correctly
- [ ] Save button appears when complete
- [ ] Save request succeeds
- [ ] Post appears in dashboard after save
- [ ] Dashboard displays all saved posts
- [ ] View modal shows complete post
- [ ] Copy to clipboard works
- [ ] Error handling works correctly
- [ ] Redirect to dashboard works

## Environment Configuration

Required environment variables:
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
DATABASE_URL=sqlite:///hiring_assistant.db
OPENAI_API_KEY=your-key-here
```

## Files Modified

1. `frontend/components/PreviewPanel.tsx` - Added redirect after save
2. `frontend/app/globals.css` - Updated dashboard styling (professional modern design)
3. `backend/routes.py` - Save post and get posts endpoints (already implemented)

## Commit History

```
feat: update dashboard and preview panel styling, add save redirect to dashboard
- Updated dashboard container with gradient backgrounds
- Enhanced post cards with modern styling
- Added smooth transitions and hover effects
- Updated button styling with Rolevate theme colors
- Added redirect to dashboard after successful save
- Improved modal styling and typography
```
