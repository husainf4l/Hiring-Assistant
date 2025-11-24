'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { JobPost } from '@/types';
import { savePost } from '@/lib/api';

interface PreviewPanelProps {
  jobPost: JobPost;
  isComplete: boolean;
  onRegenerateSection?: (sectionType: string) => void;
  sessionId?: string | null;
}

export default function PreviewPanel({ 
  jobPost, 
  isComplete, 
  onRegenerateSection,
  sessionId 
}: PreviewPanelProps) {
  const router = useRouter();
  const [isSaving, setIsSaving] = useState(false);
  const [isRegenerating, setIsRegenerating] = useState<string | null>(null);
  
  // Show preview even if empty (template mode)
  const hasContent = true;

  const handleSave = async () => {
    if (!sessionId) {
      alert('No active session');
      return;
    }

    setIsSaving(true);
    try {
      // For now, use a default user_id. In production, get from auth
      await savePost(sessionId, 1);
      alert('Post saved successfully!');
      
      // Redirect to dashboard after successful save
      setTimeout(() => {
        router.push('/dashboard');
      }, 500);
    } catch (error) {
      console.error('Failed to save post:', error);
      alert('Failed to save post. Please try again.');
    } finally {
      setIsSaving(false);
    }
  };

  const handleRegenerate = async (sectionType: string) => {
    if (!onRegenerateSection) return;
    
    setIsRegenerating(sectionType);
    try {
      await onRegenerateSection(sectionType);
    } catch (error) {
      console.error('Failed to regenerate section:', error);
    } finally {
      setIsRegenerating(null);
    }
  };

  const handleCopyToClipboard = () => {
    const postText = formatPostForCopy(jobPost);
    navigator.clipboard.writeText(postText);
    alert('Post copied to clipboard!');
  };

  const formatPostForCopy = (post: JobPost): string => {
    let text = '';
    if (post.title) text += `${post.title}\n\n`;
    if (post.summary) text += `${post.summary}\n\n`;
    
    if (post.responsibilities.length > 0) {
      text += 'Responsibilities:\n';
      post.responsibilities.forEach(resp => {
        text += `• ${resp}\n`;
      });
      text += '\n';
    }
    
    if (post.requirements.length > 0) {
      text += 'Requirements:\n';
      post.requirements.forEach(req => {
        text += `• ${req}\n`;
      });
      text += '\n';
    }
    
    if (post.skills.length > 0) {
      text += `Skills: ${post.skills.join(', ')}\n\n`;
    }
    
    if (post.hashtags.length > 0) {
      text += post.hashtags.map(h => `#${h}`).join(' ') + '\n';
    }
    
    return text;
  };

  return (
    <div className="preview-panel">
      <div className="preview-header">
        <h2>Live Preview</h2>
        <p className="subtitle">Your LinkedIn hiring post</p>
        {isComplete && <span className="badge">Complete</span>}
      </div>

      <div className="preview-content">
        <div className="linkedin-post">
          {/* Job Title */}
          <div className={`post-title-container ${!jobPost.title ? 'placeholder' : ''}`}>
            <h1 className="post-title">
              {jobPost.title || 'Position Title'}
            </h1>
          </div>

          {/* Hero Section - Job Details */}
          <div className={`job-details-hero ${!jobPost.company ? 'placeholder' : ''}`}>
            <div className="job-details-section">
              <h4 className="job-detail-label">Job details</h4>
            </div>

            <div className="job-details-grid">
              <div className="job-detail-item">
                <div className="job-detail-content">
                  <h5 className="job-detail-key">Job title</h5>
                  <p className="job-detail-value">
                    {jobPost.title || 'Artificial Intelligence Engineer'}
                  </p>
                </div>
              </div>

              <div className="job-detail-item">
                <div className="job-detail-content">
                  <h5 className="job-detail-key">Company</h5>
                  <p className="job-detail-value">
                    {jobPost.company || 'Margo Group'}
                  </p>
                </div>
              </div>

              <div className="job-detail-item">
                <div className="job-detail-content">
                  <h5 className="job-detail-key">Workplace type</h5>
                  <p className="job-detail-value">
                    {jobPost.workplace_type || 'On-site'}
                  </p>
                </div>
              </div>

              <div className="job-detail-item">
                <div className="job-detail-content">
                  <h5 className="job-detail-key">Job location</h5>
                  <p className="job-detail-value">
                    {jobPost.location || 'Amman, Jordan'}
                  </p>
                </div>
              </div>

              <div className="job-detail-item">
                <div className="job-detail-content">
                  <h5 className="job-detail-key">Job type</h5>
                  <p className="job-detail-value">
                    {jobPost.job_type || 'Full-time'}
                  </p>
                </div>
              </div>
            </div>
          </div>

            {/* Summary/Intro */}
            <div className={`post-section ${!jobPost.summary ? 'placeholder' : ''}`}>
              <div className="section-header">
                <h3 className="section-title">Summary</h3>
                {onRegenerateSection && jobPost.summary && (
                  <button
                    onClick={() => handleRegenerate('summary')}
                    disabled={isRegenerating === 'summary'}
                    className="regenerate-button"
                  >
                    {isRegenerating === 'summary' ? 'Regenerating...' : 'Regenerate'}
                  </button>
                )}
              </div>
              <p className="post-summary">
                {jobPost.summary || 'Company overview and position summary will appear here...'}
              </p>
            </div>

            {/* Company Culture & Team */}
            <div className={`post-section ${!jobPost.culture_and_team ? 'placeholder' : ''}`}>
              <div className="section-header">
                <h3 className="section-title">Company Culture & Team</h3>
                {onRegenerateSection && jobPost.culture_and_team && (
                  <button
                    onClick={() => handleRegenerate('culture_and_team')}
                    disabled={isRegenerating === 'culture_and_team'}
                    className="regenerate-button"
                  >
                    {isRegenerating === 'culture_and_team' ? 'Regenerating...' : 'Regenerate'}
                  </button>
                )}
              </div>
              <p className="post-summary">
                {jobPost.culture_and_team || 'Information about company culture and team environment will appear here...'}
              </p>
            </div>

            {/* Responsibilities */}
            <div className={`post-section ${jobPost.responsibilities.length === 0 ? 'placeholder' : ''}`}>
              <div className="section-header">
                <h3 className="section-title">Responsibilities</h3>
                {onRegenerateSection && jobPost.responsibilities.length > 0 && (
                  <button
                    onClick={() => handleRegenerate('responsibilities')}
                    disabled={isRegenerating === 'responsibilities'}
                    className="regenerate-button"
                  >
                    {isRegenerating === 'responsibilities' ? 'Regenerating...' : 'Regenerate'}
                  </button>
                )}
              </div>
              <ul className="post-list">
                {jobPost.responsibilities.length > 0 ? (
                  jobPost.responsibilities.map((resp, index) => (
                    <li key={index}>{resp}</li>
                  ))
                ) : (
                  <>
                    <li>Day-to-day responsibilities...</li>
                    <li>Key projects and goals...</li>
                    <li>Technical contributions...</li>
                  </>
                )}
              </ul>
            </div>

            {/* Requirements */}
            <div className={`post-section ${jobPost.requirements.length === 0 ? 'placeholder' : ''}`}>
              <div className="section-header">
                <h3 className="section-title">Requirements</h3>
                {onRegenerateSection && jobPost.requirements.length > 0 && (
                  <button
                    onClick={() => handleRegenerate('requirements')}
                    disabled={isRegenerating === 'requirements'}
                    className="regenerate-button"
                  >
                    {isRegenerating === 'requirements' ? 'Regenerating...' : 'Regenerate'}
                  </button>
                )}
              </div>
              <ul className="post-list">
                {jobPost.requirements.length > 0 ? (
                  jobPost.requirements.map((req, index) => (
                    <li key={index}>{req}</li>
                  ))
                ) : (
                  <>
                    <li>Required experience and skills...</li>
                    <li>Education and certifications...</li>
                    <li>Must-have qualifications...</li>
                  </>
                )}
              </ul>
            </div>

            {/* Skills */}
            <div className={`post-section ${jobPost.skills.length === 0 ? 'placeholder' : ''}`}>
              <div className="section-header">
                <h3 className="section-title">Skills</h3>
                {onRegenerateSection && jobPost.skills.length > 0 && (
                  <button
                    onClick={() => handleRegenerate('skills')}
                    disabled={isRegenerating === 'skills'}
                    className="regenerate-button"
                  >
                    {isRegenerating === 'skills' ? 'Regenerating...' : 'Regenerate'}
                  </button>
                )}
              </div>
              <div className="skills-tags">
                {jobPost.skills.length > 0 ? (
                  jobPost.skills.map((skill, index) => (
                    <span key={index} className="skill-tag">{skill}</span>
                  ))
                ) : (
                  <>
                    <span className="skill-tag placeholder-tag">Python</span>
                    <span className="skill-tag placeholder-tag">React</span>
                    <span className="skill-tag placeholder-tag">Leadership</span>
                  </>
                )}
              </div>
            </div>

            {/* Keywords */}
            <div className={`post-section ${jobPost.keywords.length === 0 ? 'placeholder' : ''}`}>
              <h3 className="section-title">Keywords</h3>
              <div className="keywords-list">
                {jobPost.keywords.length > 0 ? (
                  jobPost.keywords.map((keyword, index) => (
                    <span key={index} className="keyword">{keyword}</span>
                  ))
                ) : (
                  <>
                    <span className="keyword placeholder-keyword">hiring</span>
                    <span className="keyword placeholder-keyword">recruitment</span>
                    <span className="keyword placeholder-keyword">positions</span>
                  </>
                )}
              </div>
            </div>

            {/* Hashtags */}
            <div className={`post-section ${jobPost.hashtags.length === 0 ? 'placeholder' : ''}`}>
              <div className="hashtags">
                {jobPost.hashtags.length > 0 ? (
                  jobPost.hashtags.map((hashtag, index) => (
                    <span key={index} className="hashtag">#{hashtag}</span>
                  ))
                ) : (
                  <>
                    <span className="hashtag placeholder-hashtag">#hiring</span>
                    <span className="hashtag placeholder-hashtag">#linkedinjobs</span>
                    <span className="hashtag placeholder-hashtag">#careers</span>
                  </>
                )}
              </div>
            </div>

            {/* Action Buttons */}
            {isComplete && (
              <div className="post-section cta-section">
                <div className="action-buttons">
                  <button 
                    onClick={handleSave}
                    disabled={isSaving}
                    className="save-button"
                  >
                    {isSaving ? 'Saving...' : 'Save Post'}
                  </button>
                  <button 
                    onClick={handleCopyToClipboard}
                    className="copy-button"
                  >
                    Copy to Clipboard
                  </button>
                </div>
                <button className="cta-button">Apply Now</button>
              </div>
            )}
          </div>
      </div>
    </div>
  );
}

