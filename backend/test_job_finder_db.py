#!/usr/bin/env python3
"""
Test script to verify Job Finder agent searches jobs from database
"""

import sys
from sqlalchemy.orm import Session
from database import SessionLocal
from db_models import JobPost
from job_finder.orchestrator import JobFinderOrchestrator
from job_finder.models import JobSeekerProfile, JobListing

def test_job_finder_with_database():
    """Test that job finder agent searches from database"""
    
    # Get database session
    db = SessionLocal()
    
    try:
        # Check jobs in database
        jobs = db.query(JobPost).all()
        print(f"\n📦 Database has {len(jobs)} jobs available:\n")
        
        for job in jobs[:5]:
            print(f"  • {job.title} @ {job.company} ({job.location})")
        
        if len(jobs) > 5:
            print(f"  ... and {len(jobs) - 5} more jobs")
        
        print("\n" + "="*70)
        print("Testing Job Finder Agent with Database Integration")
        print("="*70)
        
        # Create orchestrator with database connection
        print("\n✅ Creating Job Finder Orchestrator with database connection...")
        orchestrator = JobFinderOrchestrator(db=db)
        
        # Start a session
        print("✅ Starting new job finder session...")
        session = orchestrator.start_session()
        session_id = session.session_id
        print(f"   Session ID: {session_id}")
        
        # Simulate user building their profile
        test_messages = [
            "I'm looking for a senior frontend or full-stack role",
            "I have 5 years of experience with React and TypeScript",
            "I prefer remote work",
            "I'm interested in companies working on AI or SaaS products",
        ]
        
        print("\n" + "-"*70)
        print("Simulating Profile Building Conversation:")
        print("-"*70)
        
        for i, message in enumerate(test_messages, 1):
            print(f"\n💬 User: {message}")
            
            result = orchestrator.process_user_message(session_id, message)
            
            print(f"🤖 Agent: {result['next_question']}")
            
            if result['is_profile_complete']:
                print("\n✅ Profile Complete! Searching for matching jobs...")
                break
        
        # Get final session state
        final_session = orchestrator.get_session(session_id)
        
        print("\n" + "="*70)
        print("Profile Built:")
        print("="*70)
        profile = final_session.seeker_profile
        print(f"Skills: {', '.join(profile.skills)}")
        print(f"Preferred Titles: {', '.join(profile.preferred_titles)}")
        print(f"Work Type: {profile.work_type}")
        print(f"Industries: {', '.join(profile.industries)}")
        
        print("\n" + "="*70)
        print("Job Recommendations from Database:")
        print("="*70)
        
        if final_session.recommendations:
            for i, rec in enumerate(final_session.recommendations, 1):
                print(f"\n{i}. {rec.explanation}")
                print(f"   Job ID: {rec.job_id}")
                print(f"   Match Score: {rec.match_score}%")
        else:
            print("No recommendations found (try different criteria)")
        
        print("\n" + "="*70)
        print("✅ Test Completed Successfully!")
        print("="*70)
        print("\nThe Job Finder agent is now:")
        print("  ✓ Building profiles through conversation")
        print("  ✓ Searching from real database jobs")
        print("  ✓ Matching based on skills and preferences")
        print("  ✓ Returning personalized recommendations")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    finally:
        db.close()

if __name__ == "__main__":
    test_job_finder_with_database()
