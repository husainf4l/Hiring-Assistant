'use client';

/**
 * Dashboard Page
 * Phase 6: Frontend Structure
 * 
 * List of saved hiring posts with view, copy, and delete functionality
 */

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { getPosts, JobPost } from '@/lib/api';

export default function Dashboard() {
  const router = useRouter();
  const [posts, setPosts] = useState<JobPost[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedPost, setSelectedPost] = useState<JobPost | null>(null);

  useEffect(() => {
    loadPosts();
  }, []);

  const loadPosts = async () => {
    try {
      setIsLoading(true);
      // For now, use user_id = 1. In production, get from auth
      const response = await getPosts(1);
      setPosts(response.posts);
    } catch (error) {
      console.error('Failed to load posts:', error);
      alert('Failed to load posts. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleCopyToClipboard = (post: JobPost) => {
    const postText = formatPostForCopy(post);
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
    
    if (post.keywords.length > 0) {
      text += `Keywords: ${post.keywords.join(', ')}\n\n`;
    }
    
    if (post.hashtags.length > 0) {
      text += post.hashtags.map(h => `#${h}`).join(' ') + '\n';
    }
    
    return text;
  };

  const handleViewPost = (post: JobPost) => {
    setSelectedPost(post);
  };

  const handleCloseView = () => {
    setSelectedPost(null);
  };

  if (isLoading) {
    return (
      <div className="dashboard-container">
        <div className="loading">Loading posts...</div>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>Saved Hiring Posts</h1>
        <button 
          onClick={() => router.push('/')}
          className="new-post-button"
        >
          Create New Post
        </button>
      </div>

      {selectedPost ? (
        <div className="post-view-modal">
          <div className="modal-content">
            <div className="modal-header">
              <h2>{selectedPost.title || 'Untitled Post'}</h2>
              <button onClick={handleCloseView} className="close-button">×</button>
            </div>
            <div className="post-view">
              {selectedPost.summary && (
                <div className="post-section">
                  <h3>Summary</h3>
                  <p>{selectedPost.summary}</p>
                </div>
              )}
              
              {selectedPost.responsibilities.length > 0 && (
                <div className="post-section">
                  <h3>Responsibilities</h3>
                  <ul>
                    {selectedPost.responsibilities.map((resp, index) => (
                      <li key={index}>{resp}</li>
                    ))}
                  </ul>
                </div>
              )}
              
              {selectedPost.requirements.length > 0 && (
                <div className="post-section">
                  <h3>Requirements</h3>
                  <ul>
                    {selectedPost.requirements.map((req, index) => (
                      <li key={index}>{req}</li>
                    ))}
                  </ul>
                </div>
              )}
              
              {selectedPost.skills.length > 0 && (
                <div className="post-section">
                  <h3>Skills</h3>
                  <div className="skills-tags">
                    {selectedPost.skills.map((skill, index) => (
                      <span key={index} className="skill-tag">{skill}</span>
                    ))}
                  </div>
                </div>
              )}
              
              {selectedPost.hashtags.length > 0 && (
                <div className="post-section">
                  <h3>Hashtags</h3>
                  <div className="hashtags">
                    {selectedPost.hashtags.map((hashtag, index) => (
                      <span key={index} className="hashtag">#{hashtag}</span>
                    ))}
                  </div>
                </div>
              )}
              
              <div className="post-actions">
                <button 
                  onClick={() => handleCopyToClipboard(selectedPost)}
                  className="copy-button"
                >
                  Copy to Clipboard
                </button>
              </div>
            </div>
          </div>
        </div>
      ) : (
        <div className="posts-grid">
          {posts.length === 0 ? (
            <div className="empty-state">
              <p>No saved posts yet.</p>
              <p>Create your first hiring post to get started!</p>
              <button 
                onClick={() => router.push('/')}
                className="new-post-button"
              >
                Create New Post
              </button>
            </div>
          ) : (
            posts.map((post) => (
              <div key={post.id} className="post-card">
                <h3>{post.title || 'Untitled Post'}</h3>
                {post.summary && (
                  <p className="post-preview">{post.summary.substring(0, 150)}...</p>
                )}
                <div className="post-meta">
                  {post.created_at && (
                    <span className="post-date">
                      {new Date(post.created_at).toLocaleDateString()}
                    </span>
                  )}
                </div>
                <div className="post-card-actions">
                  <button 
                    onClick={() => handleViewPost(post)}
                    className="view-button"
                  >
                    View
                  </button>
                  <button 
                    onClick={() => handleCopyToClipboard(post)}
                    className="copy-button-small"
                  >
                    Copy
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}

