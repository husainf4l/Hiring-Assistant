# Testing the Save Post Feature

## Step-by-Step Testing Guide

### Prerequisites
- Backend running: `http://localhost:8000`
- Frontend running: `http://localhost:3000`
- Browser console open (F12) for debugging

### Test Scenario 1: Complete Create Post → Save → View Dashboard

#### Step 1: Start a New Post
1. Navigate to `http://localhost:3000`
2. You should see:
   - Left panel: Chat interface with AI greeting
   - Right panel: Job post preview (template mode with placeholders)
   - Top bar: "HR Hiring Assistant" title + "View Dashboard" button

#### Step 2: Complete the Chat Conversation
1. Follow the AI prompts to provide job information:
   - Job title
   - Company name
   - Position details
   - Responsibilities
   - Requirements
   - Skills
   - etc.

2. Watch the right panel update in real-time as you provide information

#### Step 3: Wait for Completion
1. When all required information is provided, the chat should indicate "complete"
2. In the Preview Panel, you should see:
   - "Complete" badge appear at the top
   - "Save Post" button + "Copy to Clipboard" button appear at the bottom

#### Step 4: Save the Post
1. Click the "Save Post" button
2. You should see:
   - Button changes to "Saving..." state
   - Success alert: "Post saved successfully!"
   - After 500ms, automatic redirect to `/dashboard`

#### Step 5: Verify on Dashboard
1. Dashboard page loads with your saved post
2. You should see:
   - Dashboard header with "Saved Hiring Posts"
   - Post card with:
     - Post title
     - Summary preview (first 150 characters)
     - Creation date
     - "View" and "Copy" buttons

#### Step 6: View Full Post Details
1. Click "View" button on the post card
2. Modal opens showing:
   - Full post title
   - All sections (Summary, Responsibilities, Requirements, Skills, etc.)
   - "Copy to Clipboard" button
   - Close button (×)

### Test Scenario 2: Multiple Posts

#### Step 1: Create Second Post
1. Click "Create New Post" button in dashboard
2. Or navigate back to `http://localhost:3000`
3. Complete another post conversation
4. Save the second post

#### Step 2: Verify Dashboard Grid
1. Dashboard should show:
   - Both posts in a responsive grid
   - Each with their own card
   - Properly spaced and styled

### Test Scenario 3: Error Handling

#### Test 3.1: Network Error During Save
1. Open DevTools Network tab
2. Throttle network to "Slow 3G"
3. Try to save a post
4. Should show appropriate feedback

#### Test 3.2: Invalid Session
1. Manually delete sessionId from sessionStorage in console
2. Try to save
3. Should show error: "No active session"

### Visual Verification Checklist

#### Homepage (Create Post)
- [ ] Gradient background (white to light blue)
- [ ] Top bar has title and "View Dashboard" button
- [ ] Left panel shows chat interface
- [ ] Right panel shows job preview
- [ ] Messages display with proper avatars (You/AI)
- [ ] Send button has indigo gradient
- [ ] Buttons have smooth hover effects

#### Preview Panel
- [ ] Background has gradient
- [ ] Post title uses gradient text
- [ ] Sections are well organized
- [ ] Regenerate buttons appear for completed sections
- [ ] Save/Copy buttons appear when complete
- [ ] Buttons have indigo gradient styling
- [ ] Buttons have hover elevation effects

#### Dashboard
- [ ] Header has gradient text title
- [ ] "Create New Post" button has indigo gradient
- [ ] Empty state shows when no posts (with dashed border)
- [ ] Post cards have subtle borders and shadows
- [ ] Cards lift up on hover
- [ ] Card titles use gradient text
- [ ] Date is displayed correctly formatted
- [ ] View/Copy buttons have proper styling

#### Modal
- [ ] Modal has backdrop blur effect
- [ ] Content is centered and readable
- [ ] Close button has indigo styling
- [ ] Sections display with proper hierarchy
- [ ] Bullet points are indigo colored
- [ ] Copy button works and shows confirmation
- [ ] Modal can be closed with × button

### Performance Checks

1. **Save Speed**
   - Save operation should complete within 2-3 seconds
   - Redirect should happen smoothly

2. **Dashboard Loading**
   - Dashboard should load posts quickly
   - Grid should render smoothly

3. **Modal Opening**
   - Modal should open without lag
   - Content should be immediately readable

### Browser Compatibility

Test on:
- [ ] Chrome/Chromium
- [ ] Firefox
- [ ] Safari
- [ ] Edge

### Responsive Design

Test on different screen sizes:
- [ ] Desktop (1920px)
- [ ] Laptop (1366px)
- [ ] Tablet (768px)
- [ ] Mobile (375px)

### API Response Validation

Check DevTools Network tab:

#### Save Post Request
```
POST /api/save-post
Headers:
  Content-Type: application/json
Body:
  {
    "session_id": "uuid...",
    "user_id": 1
  }
Response (200):
  {
    "message": "Post saved successfully",
    "job_post": { /* full post data */ }
  }
```

#### Get Posts Request
```
GET /api/posts?user_id=1&skip=0&limit=100
Response (200):
  {
    "posts": [ /* array of posts */ ],
    "total": 1
  }
```

### Console Checks

No errors should appear in browser console:
- [ ] No 404 errors
- [ ] No CORS errors
- [ ] No JavaScript errors
- [ ] All API calls successful (200/201 status)

### Database Verification

Check SQLite database:
```bash
sqlite3 hiring_assistant.db "SELECT * FROM job_posts;"
```

Should show:
- [ ] Post appears in database
- [ ] user_id is set correctly
- [ ] All fields are populated
- [ ] Timestamps are correct

## Success Criteria

✅ Complete: All items checked and working
- User can create post through chat
- Post saves successfully to database
- Post appears on dashboard immediately
- Dashboard displays post with correct information
- User can view full post in modal
- Can create multiple posts and see all on dashboard
- UI is professional, modern, and responsive
- No console errors
- All buttons have proper hover states
- Styling matches Rolevate theme

## Known Issues / Limitations

1. **User ID**: Currently hardcoded to 1 (should use authentication)
2. **Editing**: Cannot edit saved posts (feature for future)
3. **Deleting**: Cannot delete posts (feature for future)
4. **Export**: Cannot export in different formats (feature for future)

## Troubleshooting

### Backend not responding
```bash
# Check if backend is running
curl http://localhost:8000/health

# Restart backend
cd /home/husain/hiring-assistant/backend
source ../venv/bin/activate
python -m uvicorn main:app --reload
```

### Frontend not showing changes
```bash
# Clear browser cache
# Hard refresh: Ctrl+Shift+R (or Cmd+Shift+R on Mac)
# Check if frontend has hot reload enabled
```

### Posts not appearing on dashboard
1. Check Network tab for failed requests
2. Check browser console for errors
3. Verify database has the saved post:
   ```bash
   sqlite3 hiring_assistant.db "SELECT COUNT(*) FROM job_posts;"
   ```

### Save button not appearing
1. Chat may not be complete - continue conversation
2. Check console for errors in is_complete status
3. Verify job_post exists in state

## Next Steps

After verifying the save feature works:
1. Commit changes to version control
2. Deploy to staging environment
3. Perform UAT (User Acceptance Testing)
4. Gather user feedback
5. Implement enhancement suggestions
