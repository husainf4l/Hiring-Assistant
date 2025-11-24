'use client';

import { useEffect, useMemo, useState } from 'react';
import { ChatMessage, JobRecommendation, JobSeekerProfile } from '@/types';
import JobFinderChatPanel from '@/components/jobFinder/JobFinderChatPanel';
import JobRecommendationPanel from '@/components/jobFinder/JobRecommendationPanel';
import FiltersBar from '@/components/jobFinder/FiltersBar';

const DEFAULT_AGENT_MESSAGES = [
  'Hi there! I’m your Job Finder Agent. Let’s build your profile.',
  'What kind of roles are you currently targeting?',
];

const SAMPLE_JOBS: JobRecommendation[] = [
  {
    id: 'job-1',
    title: 'Senior Frontend Engineer',
    company: 'Nova Labs',
    location: 'Remote (US)',
    requiredSkills: ['React', 'TypeScript', 'Design Systems'],
    matchPercentage: 88,
    explanation:
      'Matches your React expertise and remote preference. Team builds design systems at scale.',
    workType: 'Remote',
    salaryRange: '$150k - $170k',
  },
  {
    id: 'job-2',
    title: 'Product Designer (Growth)',
    company: 'Atlas AI',
    location: 'Austin, TX (Hybrid)',
    requiredSkills: ['Figma', 'User Research', 'Prototyping'],
    matchPercentage: 82,
    explanation:
      'Strong match on growth-focused design projects and hybrid work style.',
    workType: 'Hybrid',
    salaryRange: '$120k - $140k',
  },
  {
    id: 'job-3',
    title: 'Data Analyst',
    company: 'BluePeak Consulting',
    location: 'New York, NY (On-site)',
    requiredSkills: ['SQL', 'Looker', 'Storytelling'],
    matchPercentage: 74,
    explanation:
      'You mentioned BI storytelling experience and interest in data-heavy roles.',
    workType: 'On-site',
    salaryRange: '$100k - $120k',
  },
];

export default function JobFinderPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [profile, setProfile] = useState<JobSeekerProfile>({
    skills: [],
    preferredTitles: [],
    preferredLocations: [],
    industries: [],
  });
  const [recommendations, setRecommendations] = useState<JobRecommendation[]>([]);
  const [savedJobIds, setSavedJobIds] = useState<Set<string>>(new Set());
  const [isLoading, setIsLoading] = useState(false);
  const [filters, setFilters] = useState([
    { type: 'remote', value: 'Remote only', active: false },
    { type: 'onsite', value: 'On-site', active: false },
    { type: 'skill', value: 'React', active: false },
    { type: 'skill', value: 'Design', active: false },
  ]);

  useEffect(() => {
    // Seed chat with default agent messages
    setMessages([
      {
        role: 'assistant',
        content: DEFAULT_AGENT_MESSAGES[0],
        timestamp: new Date(),
      },
      {
        role: 'assistant',
        content: DEFAULT_AGENT_MESSAGES[1],
        timestamp: new Date(),
      },
    ]);
  }, []);

  const seekerHighlights = useMemo(() => {
    const highlights: string[] = [];
    if (profile.currentRole) highlights.push(`Current role: ${profile.currentRole}`);
    if (profile.preferredTitles.length > 0) {
      highlights.push(`Targeting: ${profile.preferredTitles.join(', ')}`);
    }
    if (profile.preferredLocations.length > 0) {
      highlights.push(`Locations: ${profile.preferredLocations.join(', ')}`);
    }
    if (profile.skills.length > 0) {
      highlights.push(`Key skills: ${profile.skills.slice(0, 4).join(', ')}`);
    }
    return highlights;
  }, [profile]);

  const toggleFilter = (index: number) => {
    setFilters((prev) =>
      prev.map((filter, i) =>
        i === index ? { ...filter, active: !filter.active } : filter
      )
    );
  };

  const handleSendMessage = async (message: string) => {
    const userMessage: ChatMessage = {
      role: 'user',
      content: message,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    // Lightweight local “matching” to simulate live updates
    setTimeout(() => {
      const lowerMessage = message.toLowerCase();
      setProfile((prev) => {
        const updated: JobSeekerProfile = { ...prev };
        if (!prev.currentRole && lowerMessage.includes('engineer')) {
          updated.currentRole = 'Software Engineer';
        }
        if (lowerMessage.includes('remote')) {
          updated.workType = 'remote';
          updated.preferredLocations = ['Remote'];
        }
        const skills = [...new Set(prev.skills)];
        ['react', 'typescript', 'design', 'sql', 'python'].forEach((skill) => {
          if (lowerMessage.includes(skill) && !skills.includes(skill)) {
            skills.push(skill);
          }
        });
        updated.skills = skills;
        return updated;
      });

      const filteredJobs = SAMPLE_JOBS.filter((job) => {
        const activeRemote = filters.find(
          (f) => f.type === 'remote' && f.active
        );
        const activeOnsite = filters.find(
          (f) => f.type === 'onsite' && f.active
        );
        if (activeRemote && job.workType !== 'Remote') {
          return false;
        }
        if (activeOnsite && job.workType === 'Remote') {
          return false;
        }
        if (profile.workType && job.workType.toLowerCase() !== profile.workType) {
          return false;
        }
        if (profile.skills.length > 0) {
          return job.requiredSkills.some((skill) =>
            profile.skills.some((seekerSkill) =>
              skill.toLowerCase().includes(seekerSkill.toLowerCase())
            )
          );
        }
        return true;
      });

      setRecommendations(filteredJobs.length ? filteredJobs : SAMPLE_JOBS);

      const agentMessage: ChatMessage = {
        role: 'assistant',
        content:
          'Thanks! Noted. Tell me about your top skills or industries you enjoy working in?',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, agentMessage]);
      setIsLoading(false);
    }, 900);
  };

  const handleSaveJob = (jobId: string) => {
    setSavedJobIds((prev) => {
      const updated = new Set(prev);
      if (updated.has(jobId)) {
        updated.delete(jobId);
      } else {
        updated.add(jobId);
      }
      return updated;
    });
  };

  return (
    <main className="job-finder-container">
      <div className="job-finder-top-bar">
        <div>
          <h1>Job Finder Assistant</h1>
          <p>Chat with the agent and see live job recommendations</p>
        </div>
      </div>
      <div className="job-finder-panels">
        <section className="job-finder-left-panel">
          <JobFinderChatPanel
            messages={messages}
            onSendMessage={handleSendMessage}
            isLoading={isLoading}
            seekerHighlights={seekerHighlights}
          />
        </section>
        <section className="job-finder-right-panel">
          <FiltersBar filters={filters} onToggleFilter={toggleFilter} />
          <JobRecommendationPanel
            recommendations={recommendations}
            savedJobIds={savedJobIds}
            onSaveJob={handleSaveJob}
          />
        </section>
      </div>
    </main>
  );
}

