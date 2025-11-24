/**
 * API Service Functions
 * Phase 6: Frontend Structure
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export interface StartChatResponse {
  session_id: string;
  response: string;
  is_complete: boolean;
  job_post: any | null;
}

export interface SendMessageResponse {
  session_id: string;
  response: string;
  is_complete: boolean;
  job_post: any | null;
}

export interface PostPreviewResponse {
  session_id: string;
  job_post: any;
  is_complete: boolean;
}

export interface JobPost {
  id?: number;
  title?: string;
  summary?: string;
  responsibilities: string[];
  requirements: string[];
  skills: string[];
  keywords: string[];
  hashtags: string[];
  tone_type?: string;
  created_at?: string;
  updated_at?: string;
  user_id?: number;
}

export interface SavedPost {
  posts: JobPost[];
  total: number;
}

/**
 * Start a new chat session
 */
export async function startChat(userId?: number): Promise<StartChatResponse> {
  const response = await fetch(`${API_BASE_URL}/start-chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ user_id: userId || null }),
  });

  if (!response.ok) {
    throw new Error('Failed to start chat');
  }

  return response.json();
}

/**
 * Send a message in the chat
 */
export async function sendMessage(
  sessionId: string,
  message: string
): Promise<SendMessageResponse> {
  const response = await fetch(`${API_BASE_URL}/send-message`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      session_id: sessionId,
      message: message,
    }),
  });

  if (!response.ok) {
    throw new Error('Failed to send message');
  }

  return response.json();
}

/**
 * Get post preview for a session
 */
export async function getPostPreview(sessionId: string): Promise<PostPreviewResponse> {
  const response = await fetch(`${API_BASE_URL}/post-preview/${sessionId}`);

  if (!response.ok) {
    throw new Error('Failed to get post preview');
  }

  return response.json();
}

/**
 * Save a post to the dashboard
 */
export async function savePost(sessionId: string, userId: number): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/save-post`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      session_id: sessionId,
      user_id: userId,
    }),
  });

  if (!response.ok) {
    throw new Error('Failed to save post');
  }

  return response.json();
}

/**
 * Get all saved posts for a user
 */
export async function getPosts(userId: number, skip: number = 0, limit: number = 100): Promise<SavedPost> {
  const response = await fetch(`${API_BASE_URL}/posts?user_id=${userId}&skip=${skip}&limit=${limit}`);

  if (!response.ok) {
    throw new Error('Failed to get posts');
  }

  return response.json();
}

/**
 * Regenerate a section of the post
 */
export async function regenerateSection(
  sessionId: string,
  sectionType: string
): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/regenerate-section`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      session_id: sessionId,
      section_type: sectionType,
    }),
  });

  if (!response.ok) {
    throw new Error('Failed to regenerate section');
  }

  return response.json();
}


