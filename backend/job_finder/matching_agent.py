"""
Job Matching Agent - compares seeker profile to job listings.
Phase 3: AI Logic scaffolding
"""

from __future__ import annotations

from typing import List, Optional, Any

try:
    from sqlalchemy.orm import Session
except ImportError:
    Session = Any

from .models import JobListing, JobRecommendation, JobSeekerProfile


class MatchingAgent:
    """Scores jobs against a seeker profile using heuristic rules."""

    def extract_filter_options(self, jobs: List[JobListing]) -> dict:
        """
        Extract unique filter options from jobs (LinkedIn-style filtering).
        
        Returns a dictionary with filter categories and their options.
        """
        filter_options = {
            "locations": set(),
            "work_types": set(),
            "experience_levels": set(),
            "companies": set(),
            "skills": set(),
            "industries": set(),
        }
        
        for job in jobs:
            if job.location:
                filter_options["locations"].add(job.location)
            if job.work_type:
                filter_options["work_types"].add(job.work_type)
            if job.experience_level:
                filter_options["experience_levels"].add(job.experience_level)
            if job.company:
                filter_options["companies"].add(job.company)
            if job.required_skills:
                filter_options["skills"].update(job.required_skills)
            if job.optional_skills:
                filter_options["skills"].update(job.optional_skills)
            if job.industries:
                filter_options["industries"].update(job.industries)
        
        # Convert sets to sorted lists for consistency
        return {
            "locations": sorted(list(filter_options["locations"])),
            "work_types": sorted(list(filter_options["work_types"])),
            "experience_levels": sorted(list(filter_options["experience_levels"])),
            "companies": sorted(list(filter_options["companies"])),
            "skills": sorted(list(filter_options["skills"])),
            "industries": sorted(list(filter_options["industries"])),
        }

    def filter_jobs(
        self,
        jobs: List[JobListing],
        filters: dict
    ) -> List[JobListing]:
        """
        Filter jobs based on LinkedIn-style criteria.
        
        Supported filters:
        - locations: List of location strings
        - work_types: List of work types (remote, onsite, hybrid)
        - experience_levels: List of experience levels
        - companies: List of company names
        - skills: List of required skills (at least one must match)
        - industries: List of industries
        - salary_min: Minimum salary
        - salary_max: Maximum salary
        - keyword: Search keyword in title/description
        """
        if not filters:
            return jobs
        
        filtered = jobs
        
        # Filter by locations
        if filters.get("locations"):
            location_filter = [loc.lower() for loc in filters["locations"]]
            filtered = [
                job for job in filtered
                if any(loc in job.location.lower() for loc in location_filter)
            ]
        
        # Filter by work types
        if filters.get("work_types"):
            work_type_filter = [wt.lower() for wt in filters["work_types"]]
            filtered = [
                job for job in filtered
                if job.work_type and job.work_type.lower() in work_type_filter
            ]
        
        # Filter by experience levels
        if filters.get("experience_levels"):
            exp_filter = [exp.lower() for exp in filters["experience_levels"]]
            filtered = [
                job for job in filtered
                if job.experience_level and job.experience_level.lower() in exp_filter
            ]
        
        # Filter by companies
        if filters.get("companies"):
            company_filter = [c.lower() for c in filters["companies"]]
            filtered = [
                job for job in filtered
                if any(c in job.company.lower() for c in company_filter)
            ]
        
        # Filter by skills (at least one match)
        if filters.get("skills"):
            skill_filter = [s.lower() for s in filters["skills"]]
            filtered = [
                job for job in filtered
                if any(
                    s.lower() in skill_filter
                    for s in (job.required_skills + job.optional_skills)
                )
            ]
        
        # Filter by industries
        if filters.get("industries"):
            industry_filter = [ind.lower() for ind in filters["industries"]]
            filtered = [
                job for job in filtered
                if job.industries and any(
                    ind.lower() in industry_filter for ind in job.industries
                )
            ]
        
        # Filter by keyword search
        if filters.get("keyword"):
            keyword = filters["keyword"].lower()
            filtered = [
                job for job in filtered
                if keyword in job.title.lower()
                or (job.description and keyword in job.description.lower())
            ]
        
        return filtered

    def score_job(self, seeker: JobSeekerProfile, job: JobListing) -> int:
        score = 0
        seeker_skills = {s.lower() for s in seeker.skills}
        job_required = {s.lower() for s in job.required_skills}
        job_optional = {s.lower() for s in job.optional_skills}

        # Skill matching (most important)
        skill_overlap = seeker_skills & job_required
        optional_overlap = seeker_skills & job_optional
        
        # Required skill matches are worth more
        required_skill_score = min(len(skill_overlap) * 20, 60)
        optional_skill_score = min(len(optional_overlap) * 8, 20)
        score += required_skill_score + optional_skill_score

        # Title matching - check if user's preferred titles match job title
        title_match = False
        if seeker.preferred_titles:
            job_title_lower = job.title.lower()
            for title in seeker.preferred_titles:
                title_lower = title.lower()
                # Match "full stack" in job title, or "frontend", "backend", etc.
                if (title_lower in job_title_lower or 
                    job_title_lower in title_lower or
                    (title_lower == "full stack" and "full stack" in job_title_lower)):
                    score += 30  # Strong boost for title match
                    title_match = True
                    break
        
        # If no exact title match but job is clearly tech/developer related
        if not title_match:
            tech_keywords = ["engineer", "developer", "architect", "programmer"]
            if any(kw in job.title.lower() for kw in tech_keywords):
                score += 5  # Small bonus for tech roles

        # Work type matching (high importance)
        if seeker.work_type and job.work_type:
            seeker_type = seeker.work_type.lower()
            job_type = job.work_type.lower()
            
            if seeker_type == job_type:
                score += 25  # Exact match
            elif seeker_type == "onsite" and job_type in ["onsite", "on-site"]:
                score += 25
            elif job_type == "remote":
                score += 15  # Remote is often acceptable
            elif job_type == "hybrid":
                score += 10  # Hybrid is partially acceptable

        # Location matching (high importance)
        if seeker.preferred_locations and job.location:
            seeker_locs = {loc.lower() for loc in seeker.preferred_locations}
            job_loc_lower = job.location.lower()
            
            for loc in seeker_locs:
                # Check if location is mentioned in job location
                if loc in job_loc_lower:
                    score += 35  # Strong location match (highest weight)
                    break
            else:
                # Check if it's remote and user accepts remote
                if "remote" in job_loc_lower and any("remote" in loc.lower() for loc in seeker_locs):
                    score += 20

        # Industry matching
        if seeker.industries and job.industries:
            industry_overlap = set(i.lower() for i in seeker.industries) & set(
                i.lower() for i in job.industries
            )
            if industry_overlap:
                score += 10

        return min(score, 100)


    def get_jobs_from_database(self, db: Any) -> List[JobListing]:
        """
        Fetch job listings from the database and convert them to JobListing models.
        Falls back to sample jobs if database is not available.
        """
        if db is None:
            # Import sample jobs as fallback
            from .models import SAMPLE_JOB_LISTINGS
            return SAMPLE_JOB_LISTINGS
        
        try:
            # Import at function level to avoid circular imports
            try:
                from ..db_models import JobPost
            except ImportError:
                from db_models import JobPost
            
            # Query all job posts from database
            db_jobs = db.query(JobPost).all()
            
            if not db_jobs:
                # If no jobs in database, return sample jobs
                from .models import SAMPLE_JOB_LISTINGS
                return SAMPLE_JOB_LISTINGS
            
            # Convert database JobPost objects to JobListing models
            job_listings = []
            for job in db_jobs:
                listing = JobListing(
                    id=str(job.id),
                    title=job.title or "",
                    company=job.company or "",
                    location=job.location or "",
                    required_skills=job.requirements if isinstance(job.requirements, list) else [],
                    optional_skills=job.skills if isinstance(job.skills, list) else [],
                    experience_level=None,
                    salary_range=None,
                    work_type=job.workplace_type or "",
                    industries=[],
                    description=job.summary or "",
                    created_at=job.created_at or None
                )
                job_listings.append(listing)
            
            return job_listings if job_listings else SAMPLE_JOB_LISTINGS
        
        except Exception as e:
            print(f"Error fetching jobs from database: {e}")
            # Fallback to sample jobs on error
            from .models import SAMPLE_JOB_LISTINGS
            return SAMPLE_JOB_LISTINGS

    def match_jobs(
        self,
        seeker: JobSeekerProfile,
        jobs: List[JobListing],
    ) -> List[JobRecommendation]:
        recommendations: List[JobRecommendation] = []
        for job in jobs:
            score = self.score_job(seeker, job)
            # Lower threshold from 40 to 30 to accommodate more matches
            if score < 30:
                continue
            explanation = self.build_explanation(seeker, job, score)
            recommendations.append(
                JobRecommendation(
                    id=f"rec-{job.id}-{seeker.id or 'anon'}",
                    job_id=job.id,
                    seeker_id=seeker.id or "anonymous",
                    match_score=score,
                    explanation=explanation,
                )
            )
        recommendations.sort(key=lambda rec: rec.match_score, reverse=True)
        return recommendations[:5]

    @staticmethod
    def build_explanation(
        seeker: JobSeekerProfile,
        job: JobListing,
        score: int,
    ) -> str:
        reasons = []
        overlap = set(seeker.skills) & set(job.required_skills)
        if overlap:
            reasons.append(f"Matches your {', '.join(overlap)} skills")
        if seeker.work_type and job.work_type:
            if seeker.work_type.lower() == job.work_type.lower():
                reasons.append(f"{job.work_type.title()} role")
        if not reasons:
            reasons.append("Strong overlap with your preferences")
        return f"{score}% match. " + ". ".join(reasons)

