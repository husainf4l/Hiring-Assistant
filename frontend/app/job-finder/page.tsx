'use client';

import { useState, useEffect } from 'react';
import ChatPanel from '@/components/ChatPanel';
import { ChatMessage } from '@/types';

interface JobData {
  id: string;
  title?: string;
  company?: string;
  location?: string;
  summary?: string;
  responsibilities?: string[];
  requirements?: string[];
  skills?: string[];
  work_type?: string;
  experience_level?: string;
}

interface Filters {
  locations?: string[];
  work_types?: string[];
  experience_levels?: string[];
  companies?: string[];
  skills?: string[];
  industries?: string[];
  keyword?: string;
}

interface FilterOptions {
  locations: string[];
  work_types: string[];
  experience_levels: string[];
  companies: string[];
  skills: string[];
  industries: string[];
}

export default function JobFinderPage() {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [jobRecommendations, setJobRecommendations] = useState<JobData[]>([]);
  const [isComplete, setIsComplete] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isInitializing, setIsInitializing] = useState(true);
  const [matchScores, setMatchScores] = useState<{ [key: string]: number }>({});
  
  // Filter state
  const [filterOptions, setFilterOptions] = useState<FilterOptions | null>(null);
  const [activeFilters, setActiveFilters] = useState<Filters>({});
  const [expandedFilter, setExpandedFilter] = useState<string | null>(null);

  // Initialize chat session
  useEffect(() => {
    const initializeChat = async () => {
      try {
        setIsInitializing(true);
        const response = await fetch('http://localhost:8000/job-finder/start-chat', {
          method: 'POST',
        });
        const data = await response.json();
        setSessionId(data.session_id);

        const initialMessage: ChatMessage = {
          role: 'assistant',
          content: data.message,
          timestamp: new Date(),
        };
        setMessages([initialMessage]);

        // Load filter options
        const filtersResponse = await fetch('http://localhost:8000/job-finder/filters');
        const filters = await filtersResponse.json();
        setFilterOptions(filters);
      } catch (error: any) {
        console.error('Failed to initialize:', error);
        alert(`Failed to start: ${error?.message}. Backend server must be running at http://localhost:8000`);
      } finally {
        setIsInitializing(false);
      }
    };

    initializeChat();
  }, []);

  const handleSendMessage = async (message: string) => {
    if (!sessionId) return;

    const userMessage: ChatMessage = {
      role: 'user',
      content: message,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/job-finder/send-message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId, message }),
      });

      const data = await response.json();
      const aiMessage: ChatMessage = {
        role: 'assistant',
        content: data.next_question,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, aiMessage]);

      if (data.is_profile_complete) {
        setIsComplete(true);
        await performSearch();
      }
    } catch (error) {
      console.error('Failed to send message:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const performSearch = async (filters?: Filters) => {
    if (!sessionId) return;

    try {
      const response = await fetch('http://localhost:8000/job-finder/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          filters: filters || activeFilters,
        }),
      });

      const data = await response.json();
      const jobs = data.recommendations || [];

      // Extract match scores
      const scores: { [key: string]: number } = {};
      jobs.forEach((rec: any) => {
        scores[rec.job_id] = rec.match_score;
      });
      setMatchScores(scores);

      // Map to JobData
      const jobList = jobs.map((rec: any) => ({
        id: rec.job_id,
        title: rec.job?.title || 'Unknown',
        company: rec.job?.company || 'Unknown',
        location: rec.job?.location || 'Unknown',
        summary: `${rec.match_score}% match`,
        skills: rec.job?.required_skills || [],
        work_type: rec.job?.work_type,
        experience_level: rec.job?.experience_level,
      }));

      setJobRecommendations(jobList);
    } catch (error) {
      console.error('Search failed:', error);
    }
  };

  const toggleFilter = (category: string, value: string) => {
    const currentValues = activeFilters[category as keyof Filters] || [];
    let newValues: string[];

    if (Array.isArray(currentValues) && currentValues.includes(value)) {
      newValues = currentValues.filter((v) => v !== value);
    } else {
      newValues = [...(Array.isArray(currentValues) ? currentValues : []), value];
    }

    const newFilters = {
      ...activeFilters,
      [category]: newValues.length > 0 ? newValues : undefined,
    };

    setActiveFilters(newFilters);
    performSearch(newFilters);
  };

  const clearAllFilters = () => {
    setActiveFilters({});
    performSearch({});
  };

  const FilterCategory = ({ title, category }: { title: string; category: keyof FilterOptions }) => {
    if (!filterOptions?.[category] || filterOptions[category].length === 0) return null;

    const isExpanded = expandedFilter === category;
    const options = filterOptions[category];
    const selectedCount = (activeFilters[category] as string[] | undefined)?.length || 0;

    return (
      <div className="filter-category">
        <button
          className="filter-header"
          onClick={() => setExpandedFilter(isExpanded ? null : category)}
        >
          <span className="filter-title">
            {title}
            {selectedCount > 0 && <span className="filter-badge">{selectedCount}</span>}
          </span>
          <span className="filter-arrow">{isExpanded ? '▼' : '▶'}</span>
        </button>

        {isExpanded && (
          <div className="filter-options">
            {options.map((option) => {
              const isSelected = (activeFilters[category] as string[] | undefined)?.includes(option);
              return (
                <label key={option} className="filter-option">
                  <input
                    type="checkbox"
                    checked={isSelected || false}
                    onChange={() => toggleFilter(category, option)}
                  />
                  <span>{option}</span>
                </label>
              );
            })}
          </div>
        )}
      </div>
    );
  };

  return (
    <main className="main-container">
      <div className="top-bar">
        <div>
          <h1>Job Finder Agent</h1>
          <p className="top-bar-subtitle">Build your profile • Get matched with jobs</p>
        </div>
        {isComplete && (
          <div className="top-bar-stats">
            <div className="stat">
              <span className="stat-label">Matches Found</span>
              <span className="stat-value">{jobRecommendations.length}</span>
            </div>
          </div>
        )}
      </div>

      <div className="panels-container">
        {/* Left Panel - Chat */}
        <section className="left-panel">
          <ChatPanel
            messages={messages}
            onSendMessage={handleSendMessage}
            isLoading={isLoading}
            title="Job Finder Agent"
            subtitle="Build your profile • Get matched with jobs"
            emptyStateMessages={[
              "Hi! I'm your Job Finder Agent.",
              "Let's build your profile together.",
              "Answer a few questions about your job preferences and I'll find the best matches for you!"
            ]}
          />
        </section>

        {/* Right Panel - Jobs List with Filters */}
        <section className="right-panel">
          {isComplete ? (
            <div className="preview-wrapper">
              <div className="preview-header">
                <h3>Filtered Jobs ({jobRecommendations.length})</h3>
              </div>

              {/* Jobs List */}
              <div className="jobs-list">
                {jobRecommendations.map((job) => (
                  <div key={job.id} className="job-card">
                    <div className="job-match-indicator" style={{
                      width: `${Math.min(matchScores[job.id] || 0, 100)}%`
                    }}></div>
                    
                    <div className="job-content">
                      <div className="job-top-row">
                        <div className="job-title-section">
                          <h3 className="job-title">{job.title}</h3>
                          <p className="job-company">{job.company}</p>
                        </div>
                        <span className="job-match-score">{matchScores[job.id] || 0}%</span>
                      </div>

                      <div className="job-meta">
                        {job.location && (
                          <span className="meta-item">
                            {job.location}
                          </span>
                        )}
                        {job.work_type && (
                          <span className="meta-item">
                            {job.work_type}
                          </span>
                        )}
                        {job.experience_level && (
                          <span className="meta-item">
                            {job.experience_level}
                          </span>
                        )}
                      </div>

                      {job.skills && job.skills.length > 0 && (
                        <div className="job-skills">
                          {job.skills.slice(0, 3).map((skill, idx) => (
                            <span key={idx} className="skill-badge">
                              {skill}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>

              {jobRecommendations.length === 0 && (
                <div className="no-results">
                  <p>No jobs match your filters. Try adjusting them!</p>
                </div>
              )}
            </div>
          ) : (
            <div className="preview-wrapper">
              <div className="preview-placeholder">
                <div className="placeholder-icon">🔍</div>
                <h3>Answer Questions</h3>
                <p>Complete your profile on the left to see personalized job matches.</p>
              </div>
            </div>
          )}
        </section>
      </div>

      <style jsx>{`
        .main-container {
          display: flex;
          flex-direction: column;
          height: 100vh;
          width: 100vw;
          overflow: hidden;
          background: #f5f5f5;
        }

        .top-bar {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 20px 30px;
          background: white;
          border-bottom: 1px solid #e0e0e0;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
        }

        .top-bar h1 {
          font-size: 24px;
          font-weight: 700;
          margin: 0;
          color: #1a1a1a;
        }

        .top-bar-subtitle {
          font-size: 13px;
          color: #666;
          margin: 4px 0 0 0;
        }

        .top-bar-stats {
          display: flex;
          gap: 20px;
        }

        .stat {
          display: flex;
          flex-direction: column;
          align-items: center;
        }

        .stat-label {
          font-size: 11px;
          color: #999;
          text-transform: uppercase;
          font-weight: 600;
          letter-spacing: 0.5px;
        }

        .stat-value {
          font-size: 20px;
          font-weight: 700;
          color: #0a66c2;
        }

        .panels-container {
          display: flex;
          flex: 1;
          gap: 0;
          overflow: hidden;
          width: 100%;
        }

        .left-panel {
          flex: 1;
          display: flex;
          flex-direction: column;
          background-color: #ffffff;
          min-width: 0;
          overflow: hidden;
          border-right: 2px solid #e0e0e0;
        }

        .right-panel {
          flex: 1;
          display: flex;
          flex-direction: column;
          background: #ffffff;
          min-width: 0;
          overflow-y: auto;
        }

        .preview-wrapper {
          flex: 1;
          display: flex;
          flex-direction: column;
          padding: 1.5rem;
          overflow-y: auto;
          background: var(--bg-primary);
        }

        .preview-header {
          padding: 0 0 1.5rem 0;
          border-bottom: 2px solid var(--border-light);
          margin-bottom: 1.5rem;
        }

        .preview-header h3 {
          margin: 0;
          font-size: 1.125rem;
          font-weight: 700;
          color: var(--text-primary);
          letter-spacing: -0.3px;
        }

        .preview-placeholder {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          padding: 3rem 1.5rem;
          color: var(--text-tertiary);
          text-align: center;
          flex: 1;
        }

        .placeholder-icon {
          font-size: 4rem;
          margin-bottom: 1rem;
          opacity: 0.4;
        }

        .modern-filters {
          background: #ffffff;
          border: 1px solid #e5e7eb;
          border-radius: 8px;
          padding: 16px;
          margin-bottom: 16px;
          max-height: 420px;
          overflow-y: auto;
        }

        .modern-filters::-webkit-scrollbar {
          width: 6px;
        }

        .modern-filters::-webkit-scrollbar-track {
          background: #f3f4f6;
          border-radius: 3px;
        }

        .modern-filters::-webkit-scrollbar-thumb {
          background: #d1d5db;
          border-radius: 3px;
        }

        .modern-filters::-webkit-scrollbar-thumb:hover {
          background: #9ca3af;
        }

        .filters-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 16px;
          padding-bottom: 12px;
          border-bottom: 2px solid #f0f0f0;
        }

        .filters-header h4 {
          margin: 0;
          font-size: 14px;
          font-weight: 700;
          color: #111827;
          text-transform: uppercase;
          letter-spacing: 0.5px;
        }

        .clear-filters {
          background: none;
          border: none;
          color: #3b82f6;
          cursor: pointer;
          font-size: 12px;
          font-weight: 600;
          padding: 0;
          transition: color 0.2s ease;
          text-decoration: none;
        }

        .clear-filters:hover {
          color: #1d4ed8;
          text-decoration: underline;
        }

        .filter-category {
          margin-bottom: 12px;
        }

        .filter-category:last-child {
          margin-bottom: 0;
        }

        .filter-header {
          background: #ffffff;
          border: 1px solid #e5e7eb;
          border-radius: 6px;
          padding: 11px 12px;
          cursor: pointer;
          display: flex;
          justify-content: space-between;
          align-items: center;
          width: 100%;
          font-size: 13px;
          font-weight: 600;
          color: #374151;
          transition: all 0.2s ease;
        }

        .filter-header:hover {
          background: #f9fafb;
          border-color: #d1d5db;
        }

        .filter-header:active {
          background: #f3f4f6;
        }

        .filter-title {
          display: flex;
          align-items: center;
          gap: 8px;
          color: #111827;
        }

        .filter-badge {
          background: #3b82f6;
          color: white;
          border-radius: 12px;
          padding: 2px 8px;
          font-size: 11px;
          font-weight: 700;
          min-width: 20px;
          text-align: center;
        }

        .filter-arrow {
          font-size: 11px;
          color: #9ca3af;
          transition: transform 0.2s ease;
        }

        .filter-options {
          background: #ffffff;
          border: 1px solid #e5e7eb;
          border-top: none;
          border-radius: 0 0 6px 6px;
          padding: 10px;
          margin-top: -1px;
          margin-bottom: 0;
          max-height: 220px;
          overflow-y: auto;
        }

        .filter-options::-webkit-scrollbar {
          width: 5px;
        }

        .filter-options::-webkit-scrollbar-track {
          background: #f9fafb;
        }

        .filter-options::-webkit-scrollbar-thumb {
          background: #d1d5db;
          border-radius: 2px;
        }

        .filter-option {
          display: flex;
          align-items: center;
          padding: 8px 10px;
          cursor: pointer;
          font-size: 13px;
          margin-bottom: 4px;
          border-radius: 4px;
          transition: all 0.15s ease;
          color: #374151;
        }

        .filter-option:hover {
          background: #f3f4f6;
        }

        .filter-option:last-child {
          margin-bottom: 0;
        }

        .filter-option input[type='checkbox'] {
          width: 16px;
          height: 16px;
          margin-right: 10px;
          cursor: pointer;
          accent-color: #3b82f6;
          border-radius: 3px;
          flex-shrink: 0;
        }

        .filter-option span {
          font-weight: 500;
        }

        .job-card {
          background: var(--bg-primary);
          border: 1px solid var(--border);
          border-radius: 8px;
          overflow: hidden;
          margin-bottom: 12px;
          cursor: pointer;
          transition: all 0.2s ease;
          box-shadow: var(--shadow-sm);
          position: relative;
        }

        .job-card:hover {
          border-color: var(--primary-light);
          box-shadow: var(--shadow-md);
          transform: translateY(-2px);
        }

        .job-match-indicator {
          height: 4px;
          background: linear-gradient(90deg, var(--primary-light), var(--primary-dark));
          transition: width 0.3s ease;
        }

        .job-content {
          padding: 1rem;
        }

        .job-top-row {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
          margin-bottom: 0.75rem;
          gap: 0.75rem;
        }

        .job-title-section {
          flex: 1;
        }

        .job-title {
          margin: 0;
          font-size: 0.9375rem;
          font-weight: 600;
          color: var(--text-primary);
          line-height: 1.4;
        }

        .job-company {
          margin: 0.25rem 0 0 0;
          font-size: 0.8125rem;
          color: var(--text-secondary);
          font-weight: 400;
        }

        .job-match-score {
          background: #eff6ff;
          color: var(--primary);
          padding: 0.375rem 0.75rem;
          border-radius: 6px;
          font-size: 0.8125rem;
          font-weight: 600;
          white-space: nowrap;
          border: 1px solid #bfdbfe;
        }

        .job-meta {
          display: flex;
          flex-wrap: wrap;
          gap: 0.5rem;
          margin-bottom: 0.75rem;
          font-size: 0.75rem;
        }

        .meta-item {
          display: inline-block;
          color: var(--text-secondary);
          background: var(--bg-tertiary);
          padding: 0.3125rem 0.625rem;
          border-radius: 4px;
          font-weight: 500;
          border: 1px solid var(--border);
        }

        .job-skills {
          display: flex;
          flex-wrap: wrap;
          gap: 0.375rem;
        }

        .skill-badge {
          background: var(--bg-tertiary);
          color: var(--text-primary);
          padding: 0.3125rem 0.625rem;
          border-radius: 4px;
          font-size: 0.75rem;
          font-weight: 500;
          border: 1px solid var(--border);
          transition: all 0.2s ease;
        }

        .skill-badge:hover {
          background: var(--border);
          border-color: var(--border);
        }

        .job-card:hover .skill-badge {
          background: var(--border);
        }
        }

        .job-company {
          margin: 4px 0;
          font-size: 13px;
          font-weight: 500;
          color: #666;
        }

        .no-results {
          text-align: center;
          padding: 2.5rem 1.25rem;
          color: var(--text-tertiary);
          font-size: 0.875rem;
        }

        .jobs-list {
          max-height: calc(100vh - 350px);
          overflow-y: auto;
          padding-right: 0.5rem;
        }

        .jobs-list::-webkit-scrollbar {
          width: 6px;
        }

        .jobs-list::-webkit-scrollbar-track {
          background: transparent;
        }

        .jobs-list::-webkit-scrollbar-thumb {
          background: var(--border);
          border-radius: 3px;
        }

        .jobs-list::-webkit-scrollbar-thumb:hover {
          background: var(--text-tertiary);
        }
      `}</style>
    </main>
  );
}
