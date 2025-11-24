/**
 * TypeScript types for HR Hiring Assistant
 * Phase 2: UX Structure
 */

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: Date;
}

export interface JobPost {
  id?: string;
  title?: string;
  summary?: string;
  company?: string;
  location?: string;
  workplace_type?: string; // On-site, Remote, Hybrid
  job_type?: string; // Full-time, Part-time, Contract
  culture_and_team?: string;
  responsibilities: string[];
  requirements: string[];
  skills: string[];
  keywords: string[];
  hashtags: string[];
  tone_type?: string;
}

export interface ChatSession {
  sessionId: string;
  messages: ChatMessage[];
  jobPost: JobPost;
  isComplete: boolean;
}


