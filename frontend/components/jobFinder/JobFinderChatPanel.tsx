'use client';

import { useState } from 'react';
import { ChatMessage } from '@/types';

interface JobFinderChatPanelProps {
  messages: ChatMessage[];
  onSendMessage: (message: string) => void;
  isLoading?: boolean;
  seekerHighlights: string[];
}

export default function JobFinderChatPanel({
  messages,
  onSendMessage,
  isLoading,
  seekerHighlights,
}: JobFinderChatPanelProps) {
  const [inputValue, setInputValue] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;
    onSendMessage(inputValue.trim());
    setInputValue('');
  };

  return (
    <div className="job-finder-chat-panel">
      <div className="job-finder-chat-header">
        <div>
          <h2>Job Finder Agent</h2>
          <p className="subtitle">Let’s build your profile together</p>
        </div>
        {seekerHighlights.length > 0 && (
          <div className="seeker-highlights">
            <p>Profile summary:</p>
            <ul>
              {seekerHighlights.map((highlight) => (
                <li key={highlight}>{highlight}</li>
              ))}
            </ul>
          </div>
        )}
      </div>

      <div className="job-finder-chat-messages">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.role}`}>
            <div className="message-avatar">
              {message.role === 'user' ? '👤' : '🤖'}
            </div>
            <div className="message-content">
              <div className="message-text">{message.content}</div>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message assistant">
            <div className="message-avatar">🤖</div>
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
      </div>

      <form onSubmit={handleSubmit} className="job-finder-chat-input-form">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Tell me more about your experience..."
          disabled={isLoading}
          className="chat-input"
        />
        <button
          type="submit"
          disabled={!inputValue.trim() || isLoading}
          className="send-button"
        >
          Send
        </button>
      </form>
    </div>
  );
}

