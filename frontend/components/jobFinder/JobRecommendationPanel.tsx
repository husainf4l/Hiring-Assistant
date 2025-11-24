'use client';

import { JobRecommendation } from '@/types';

interface JobRecommendationPanelProps {
  recommendations: JobRecommendation[];
  savedJobIds: Set<string>;
  onSaveJob: (jobId: string) => void;
}

export default function JobRecommendationPanel({
  recommendations,
  savedJobIds,
  onSaveJob,
}: JobRecommendationPanelProps) {
  return (
    <div className="job-recommendation-panel">
      <div className="job-recommendation-header">
        <h2>Live Job Recommendations</h2>
        <p className="subtitle">
          Personalized matches update automatically as you chat
        </p>
      </div>

      <div className="job-recommendation-content">
        {recommendations.length === 0 ? (
          <div className="empty-job-recommendations">
            <p>🧭 Start chatting to see tailored job opportunities here.</p>
          </div>
        ) : (
          recommendations.map((job) => (
            <div key={job.id} className="job-card">
              <div className="job-card-header">
                <div>
                  <h3>{job.title}</h3>
                  <p className="company">
                    {job.company} · {job.location}
                  </p>
                </div>
                <div className="match-score">
                  <span>{job.matchPercentage}%</span>
                  <p>Match</p>
                </div>
              </div>

              <div className="job-card-section">
                <p className="section-label">Required skills</p>
                <div className="skill-chips">
                  {job.requiredSkills.map((skill) => (
                    <span key={skill} className="skill-chip">
                      {skill}
                    </span>
                  ))}
                </div>
              </div>

              <div className="job-card-section">
                <p className="section-label">Why this job fits you</p>
                <p className="job-explanation">{job.explanation}</p>
              </div>

              <div className="job-card-meta">
                <span>{job.workType}</span>
                <span>{job.salaryRange}</span>
              </div>

              <div className="job-card-actions">
                <button className="ghost-button">View</button>
                <button
                  className={savedJobIds.has(job.id) ? 'save-button saved' : 'save-button'}
                  onClick={() => onSaveJob(job.id)}
                  type="button"
                >
                  {savedJobIds.has(job.id) ? 'Saved' : 'Save Job'}
                </button>
                <button className="primary-button">Apply</button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

