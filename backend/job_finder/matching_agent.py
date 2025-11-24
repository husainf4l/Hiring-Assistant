""
"Job Matching Agent - compares seeker profile to job listings."
"Phase 3: AI Logic scaffolding"
""

from __future__ import annotations

from typing import List

from .models import JobListing, JobRecommendation, JobSeekerProfile


class MatchingAgent:
    """Scores jobs against a seeker profile using heuristic rules."""

    def score_job(self, seeker: JobSeekerProfile, job: JobListing) -> int:
        score = 0
        seeker_skills = {s.lower() for s in seeker.skills}
        job_required = {s.lower() for s in job.required_skills}
        job_optional = {s.lower() for s in job.optional_skills}

        skill_overlap = seeker_skills & job_required
        optional_overlap = seeker_skills & job_optional
        score += min(len(skill_overlap) * 10, 40)
        score += min(len(optional_overlap) * 5, 15)

        if seeker.preferred_titles:
            titles = " ".join(seeker.preferred_titles).lower()
            if job.title.lower() in titles or titles in job.title.lower():
                score += 15

        if seeker.work_type and job.work_type:
            if seeker.work_type.lower() == job.work_type.lower():
                score += 20

        if seeker.preferred_locations:
            for location in seeker.preferred_locations:
                if location.lower() in job.location.lower():
                    score += 10
                    break

        if seeker.industries and job.industries:
            if set(i.lower() for i in seeker.industries) & set(
                i.lower() for i in job.industries
            ):
                score += 10

        return min(score, 100)

    def match_jobs(
        self,
        seeker: JobSeekerProfile,
        jobs: List[JobListing],
    ) -> List[JobRecommendation]:
        recommendations: List[JobRecommendation] = []
        for job in jobs:
            score = self.score_job(seeker, job)
            if score < 40:
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

