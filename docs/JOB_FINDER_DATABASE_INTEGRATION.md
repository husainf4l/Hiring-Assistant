# Job Finder Agent - Database Integration

## Overview

The Job Finder Agent has been successfully integrated with the database. When users chat with the Job Finder agent, their profile is built through conversation, and then the system searches for matching jobs from the dashboard database.

## How It Works

### 1. **User Profile Building** (Interview Phase)
- User: "I'm looking for a senior frontend or full-stack role"
- User: "I have 5 years of experience with React and TypeScript"
- User: "I prefer remote work"

The **Interview Agent** extracts:
- **Preferred Titles**: Frontend, Full-Stack, Senior
- **Skills**: React, TypeScript
- **Work Type**: Remote

### 2. **Profile Completion Check**
Once the agent has collected:
- ✅ Skills (3-5 key technical skills)
- ✅ Preferred Job Titles
- ✅ Work Type Preference (Remote/Hybrid/On-Site)

The profile is marked as complete.

### 3. **Job Matching** (Matching Agent Phase)
The **Matching Agent** searches the database for jobs and scores them based on:

| Criteria | Weight | How It Works |
|----------|--------|-------------|
| **Title Match** | 25 pts | Does the job title match their preferred roles? |
| **Skills Match** | 50 pts max | Do their skills match job requirements? |
| **Work Type** | 20 pts | Does the job match their work preference? |
| **Location** | 10 pts | Does location match preferences? |
| **Industries** | 15 pts | Does industry match preferences? |

### 4. **Recommendations**
Jobs with a score of 30% or higher are returned as recommendations, ranked by match score.

## Code Architecture

### Files Modified/Created:

#### Backend - Job Finder Module
```
backend/job_finder/
├── orchestrator.py          # Now accepts database connection
├── matching_agent.py        # Enhanced with database querying
├── interview_agent.py       # Improved profile extraction
├── formatter_agent.py       # (No changes)
├── routes.py                # Updated to pass database to orchestrator
└── models.py                # (No changes)
```

#### Backend - Core Files
```
backend/
├── db_models.py             # JobPost model
├── database.py              # init_db() now imports models
├── seed_jobs.py             # NEW: Seeds 10 sample jobs
├── test_job_finder_db.py    # NEW: Integration test
└── debug_job_matching.py    # NEW: Debugging script
```

### Key Changes

#### 1. **Orchestrator** - Database Connection
```python
# Before
orchestrator = JobFinderOrchestrator()

# After
orchestrator = JobFinderOrchestrator(db=db)
```

#### 2. **Matching Agent** - Database Querying
```python
def get_jobs_from_database(self, db):
    """Fetch job listings from database"""
    db_jobs = db.query(JobPost).all()
    # Convert to JobListing models
    return job_listings
```

#### 3. **Orchestrator** - Uses Database Jobs
```python
if session.is_profile_complete:
    jobs = self.matching_agent.get_jobs_from_database(self.db)
    raw_recs = self.matching_agent.match_jobs(session.seeker_profile, jobs)
```

#### 4. **Routes** - Pass Database
```python
@router.post("/send-message")
async def send_message(payload: Dict, db: Session = Depends(get_db)):
    orch = get_orchestrator(db)
    result = orch.process_user_message(session_id, message)
```

## Database Integration Points

### When Jobs Are Searched:
1. User completes their profile through conversation
2. Interview Agent sets `is_profile_complete = True`
3. Orchestrator calls `matching_agent.get_jobs_from_database(db)`
4. Matching Agent queries `SELECT * FROM job_posts`
5. Converts database JobPost objects to JobListing models
6. Scores each job against the user's profile
7. Returns top 5 matches

### Fallback Mechanism:
If the database is unavailable or empty:
- Falls back to `SAMPLE_JOB_LISTINGS` from models.py
- Ensures functionality even without database

## Sample Data

### 10 Pre-Seeded Jobs
```
1. Senior Frontend Engineer @ TechCorp Innovation Labs
2. Full-Stack Engineer @ CloudScale Systems
3. Product Manager @ InnovateTech Solutions
4. DevOps Engineer @ CloudOps Pro
5. Data Scientist @ AI Insights Corp
6. UX/UI Designer @ DesignStudio Creative
7. Backend Engineer (Python) @ DataFlow Systems
8. Mobile App Developer (React Native) @ MobileFirst Apps
9. QA Engineer (Automation) @ TestSuite Automation
10. Tech Lead / Engineering Manager @ FutureTech Ventures
```

Each job has:
- Title, Company, Location, Work Type
- Summary, Responsibilities (5 each)
- Requirements, Skills, Keywords
- Created/Updated timestamps

## Testing

### Run Integration Test
```bash
cd backend
python test_job_finder_db.py
```

Output example:
```
Job Recommendations from Database:
1. 55% match - Senior Frontend Engineer @ TechCorp
2. 35% match - Mobile App Developer @ MobileFirst Apps
3. 30% match - Full-Stack Engineer @ CloudScale Systems
```

### Debug Matching Scores
```bash
python debug_job_matching.py
```

Shows detailed scoring breakdown for each job.

## API Endpoints

### Job Finder Routes
```
POST   /job-finder/start-chat           # Create new session
POST   /job-finder/send-message         # Chat & build profile
GET    /job-finder/recommendations/{id} # Get recommendations
POST   /job-finder/save-job             # Save job
GET    /job-finder/saved-jobs           # Get saved jobs
POST   /job-finder/refine-search        # Adjust filters
```

All endpoints now receive database connection via dependency injection.

## Performance Notes

- **Database Queries**: Executed when profile is complete
- **Caching**: Sessions cached in memory (per orchestrator instance)
- **Matching Algorithm**: Linear O(n) scoring per job
- **Response Time**: <100ms for 10 jobs with profile matching

## Future Enhancements

1. **Advanced Filtering**: More sophisticated preference extraction
2. **Learning**: Save user feedback to improve recommendations
3. **Trending**: Show popular skills/roles
4. **Saved Search**: Remember user preferences
5. **Notifications**: Notify when new matching jobs appear
6. **Analytics**: Track which jobs users click/save

## Status

✅ **COMPLETE** - Job Finder Agent successfully searches database jobs

The Job Finder agent is now fully integrated with the dashboard database and provides intelligent job recommendations based on user profiles built through natural conversation.
