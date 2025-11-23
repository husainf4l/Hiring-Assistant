'use client';

/**
 * HR Hiring Assistant - Main Page
 * Phase 6: Frontend Structure
 * 
 * Two-panel interface:
 * - Left: AI Chat Panel
 * - Right: Live Hiring Post Preview
 */

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import ChatPanel from '@/components/ChatPanel';
import PreviewPanel from '@/components/PreviewPanel';
import { ChatMessage, JobPost } from '@/types';
import { startChat, sendMessage, getPostPreview, regenerateSection } from '@/lib/api';

export default function Home() {
  const router = useRouter();
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [jobPost, setJobPost] = useState<JobPost>({
    responsibilities: [],
    requirements: [],
    skills: [],
    keywords: [],
    hashtags: [],
  });
  const [isComplete, setIsComplete] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isInitializing, setIsInitializing] = useState(true);

  // Initialize chat session on mount
  useEffect(() => {
    const initializeChat = async () => {
      try {
        setIsInitializing(true);
        const response = await startChat();
        setSessionId(response.session_id);
        
        // Add initial AI message
        const initialMessage: ChatMessage = {
          role: 'assistant',
          content: response.response,
          timestamp: new Date(),
        };
        setMessages([initialMessage]);
      } catch (error: any) {
        console.error('Failed to initialize chat:', error);
        const errorMessage = error?.message || error?.toString() || 'Unknown error';
        console.error('Error details:', errorMessage);
        alert(`Failed to start chat: ${errorMessage}. Please check the backend server is running at http://localhost:8000`);
      } finally {
        setIsInitializing(false);
      }
    };

    initializeChat();
  }, []);

  // Poll for post preview updates
  useEffect(() => {
    if (!sessionId) return;

    const pollPreview = async () => {
      try {
        const preview = await getPostPreview(sessionId);
        if (preview.job_post) {
          setJobPost(preview.job_post);
          setIsComplete(preview.is_complete);
        }
      } catch (error) {
        console.error('Failed to get preview:', error);
      }
    };

    // Poll every 2 seconds while chat is active
    const interval = setInterval(pollPreview, 2000);
    return () => clearInterval(interval);
  }, [sessionId]);

  const handleSendMessage = async (message: string) => {
    if (!sessionId) return;

    // Add user message immediately
    const userMessage: ChatMessage = {
      role: 'user',
      content: message,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await sendMessage(sessionId, message);
      
      // Add AI response
      const aiMessage: ChatMessage = {
        role: 'assistant',
        content: response.response,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, aiMessage]);

      // Update job post if available
      if (response.job_post) {
        setJobPost(response.job_post);
      }
      
      setIsComplete(response.is_complete);
    } catch (error) {
      console.error('Failed to send message:', error);
      alert('Failed to send message. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRegenerateSection = async (sectionType: string): Promise<void> => {
    if (!sessionId) return;

    try {
      const response = await regenerateSection(sessionId, sectionType);
      if (response.job_post) {
        setJobPost(response.job_post);
      }
    } catch (error) {
      console.error('Failed to regenerate section:', error);
      alert('Failed to regenerate section. Please try again.');
      throw error;
    }
  };

  if (isInitializing) {
    return (
      <main className="main-container">
        <div style={{ 
          display: 'flex', 
          justifyContent: 'center', 
          alignItems: 'center', 
          height: '100vh',
          width: '100%'
        }}>
          <p>Initializing chat...</p>
        </div>
      </main>
    );
  }

  return (
    <main className="main-container">
      <div className="top-bar">
        <h1>HR Hiring Assistant</h1>
        <button 
          onClick={() => router.push('/dashboard')}
          className="dashboard-button"
        >
          View Dashboard
        </button>
      </div>
      <div className="panels-wrapper">
        <div className="left-panel">
          <ChatPanel
            messages={messages}
            onSendMessage={handleSendMessage}
            isLoading={isLoading}
          />
        </div>
        
        <div className="right-panel">
          <PreviewPanel 
            jobPost={jobPost} 
            isComplete={isComplete}
            onRegenerateSection={handleRegenerateSection}
            sessionId={sessionId}
          />
        </div>
      </div>
    </main>
  );
}

