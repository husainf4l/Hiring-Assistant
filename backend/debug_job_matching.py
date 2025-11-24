#!/usr/bin/env python3
"""
Debug script to check job matching details
"""

from database import SessionLocal
from db_models import JobPost
from job_finder.models import JobSeekerProfile, JobListing
from job_finder.matching_agent import MatchingAgent

def debug_job_matching():
    """Debug the matching process"""
    
    db = SessionLocal()
    
    try:
        # Get jobs from database
        db_jobs = db.query(JobPost).all()
        
        # Convert to JobListing
        matching_agent = MatchingAgent()
        job_listings = matching_agent.get_jobs_from_database(db)
        
        print(f"\n📦 Found {len(job_listings)} job listings in database\n")
        
        # Create a test profile
        profile = JobSeekerProfile(
            id="test-123",
            skills=["react", "typescript"],
            preferred_titles=["frontend", "full-stack", "senior"],
            work_type="remote",
            industries=["ai", "saas"]
        )
        
        print("👤 Test Profile:")
        print(f"   Skills: {profile.skills}")
        print(f"   Preferred Titles: {profile.preferred_titles}")
        print(f"   Work Type: {profile.work_type}")
        print(f"   Industries: {profile.industries}\n")
        
        print("="*80)
        print("Detailed Matching Scores for Each Job:")
        print("="*80 + "\n")
        
        all_scores = []
        for job in job_listings:
            score = matching_agent.score_job(profile, job)
            all_scores.append((score, job))
            
            print(f"Job: {job.title} @ {job.company}")
            print(f"Location: {job.location} | Work Type: {job.work_type}")
            print(f"Required Skills: {job.required_skills}")
            
            # Detailed scoring breakdown
            seeker_skills = set(s.lower() for s in profile.skills)
            job_required = set(s.lower() for s in job.required_skills)
            skill_overlap = seeker_skills & job_required
            
            print(f"Skill Overlap: {skill_overlap} → {len(skill_overlap) * 15} points")
            
            # Title match
            job_title_lower = job.title.lower()
            title_match = any(t.lower() in job_title_lower for t in profile.preferred_titles)
            print(f"Title Match: {title_match} → {'25 points' if title_match else '0 points'}")
            
            # Work type
            work_type_match = profile.work_type and profile.work_type.lower() == job.work_type.lower()
            print(f"Work Type Match ({profile.work_type} vs {job.work_type}): {work_type_match} → {'20 points' if work_type_match else '0 points'}")
            
            print(f"📊 **TOTAL SCORE: {score}** {'✅ MATCH' if score >= 30 else '❌ NO MATCH'}\n")
        
        print("="*80)
        print("Top Matches:")
        print("="*80 + "\n")
        
        sorted_jobs = sorted(all_scores, key=lambda x: x[0], reverse=True)
        for rank, (score, job) in enumerate(sorted_jobs[:5], 1):
            if score >= 30:
                print(f"{rank}. {job.title} @ {job.company} - Score: {score}%")
            
    finally:
        db.close()

if __name__ == "__main__":
    debug_job_matching()
