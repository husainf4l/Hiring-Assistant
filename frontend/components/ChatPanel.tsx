'use client';

import { useState } from 'react';
import { ChatMessage } from '@/types';

interface ChatPanelProps {
  messages: ChatMessage[];
  onSendMessage: (message: string) => void;
  isLoading?: boolean;
  title?: string;
  subtitle?: string;
  emptyStateMessages?: string[];
}

export default function ChatPanel({ 
  messages, 
  onSendMessage, 
  isLoading,
  title = "AI Hiring Assistant",
  subtitle = "Answer questions about your job requirements",
  emptyStateMessages = [
    "Welcome to the AI Hiring Assistant",
    "I'll guide you through a series of questions about the job, and together we'll create a professional job posting.",
    "Let's get started."
  ]
}: ChatPanelProps) {
  const [inputValue, setInputValue] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim() && !isLoading) {
      onSendMessage(inputValue.trim());
      setInputValue('');
    }
  };

  return (
    <div className="chat-panel">
      <div className="chat-header">
        <h2>{title}</h2>
        <p className="subtitle">{subtitle}</p>
      </div>

      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="empty-state">
            {emptyStateMessages.map((msg, idx) => (
              <p key={idx}>{msg}</p>
            ))}
          </div>
        ) : (
          messages.map((message, index) => (
            <div key={index} className={`message ${message.role}`}>
              <div className="message-avatar">
                {message.role === 'user' ? 'You' : 'AI'}
              </div>
              <div className="message-content">
                <div className="message-text">{message.content}</div>
              </div>
            </div>
          ))
        )}
        {isLoading && (
          <div className="message assistant">
            <div className="message-avatar">AI</div>
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

      <form onSubmit={handleSubmit} className="chat-input-form">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Type your answer here..."
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


