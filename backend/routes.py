"""
API Routes for HR Hiring Assistant
Phase 5: Backend Structure (FastAPI)
"""

import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

try:
    from .database import get_db
    from .models import (
        StartChatRequest, SendMessageRequest, PostPreviewResponse,
        SavePostRequest, RegenerateSectionRequest, JobPost, ChatMessage
    )
    from .repositories import (
        ChatSessionRepository, JobPostRepository, UserRepository,
        db_to_pydantic_job_post
    )
    from .agents.orchestrator import AgentOrchestrator
except ImportError:
    from database import get_db
    from models import (
        StartChatRequest, SendMessageRequest, PostPreviewResponse,
        SavePostRequest, RegenerateSectionRequest, JobPost, ChatMessage
    )
    from repositories import (
        ChatSessionRepository, JobPostRepository, UserRepository,
        db_to_pydantic_job_post
    )
    from agents.orchestrator import AgentOrchestrator

router = APIRouter()

# Global orchestrator instance (in production, use dependency injection)
orchestrator = None

def get_orchestrator():
    """Lazy load orchestrator to avoid startup failures"""
    global orchestrator
    if orchestrator is None:
        try:
            orchestrator = AgentOrchestrator()
            print("✓ Orchestrator initialized successfully")
        except Exception as e:
            print(f"ERROR: Failed to initialize orchestrator: {e}")
            import traceback
            traceback.print_exc()
            raise HTTPException(
                status_code=500,
                detail=f"Orchestrator initialization failed: {str(e)}"
            )
    return orchestrator


@router.post("/start-chat", response_model=dict)
async def start_chat(request: StartChatRequest, db: Session = Depends(get_db)):
    """
    Start a new job creation session
    Creates a new chat session and returns the initial AI question
    """
    # Get orchestrator (lazy-loaded)
    orch = get_orchestrator()
    
    # Generate unique session ID
    session_id = str(uuid.uuid4())
    
    # Start session with orchestrator
    orchestrator_result = orch.start_session(session_id)
    
    # Create chat session in database
    chat_session_data = {
        "session_id": session_id,
        "messages": [
            {"role": "assistant", "content": orchestrator_result["response"], "timestamp": datetime.utcnow().isoformat()}
        ],
        "job_info": {},
        "is_complete": 0,  # False
        "user_id": request.user_id
    }
    
    ChatSessionRepository.create(db, chat_session_data)
    
    return {
        "session_id": session_id,
        "response": orchestrator_result["response"],
        "is_complete": False,
        "job_post": None
    }


@router.post("/send-message", response_model=dict)
async def send_message(request: SendMessageRequest, db: Session = Depends(get_db)):
    """
    HR sends message → AI replies → returns updated preview
    Processes the user's message through the AI agents and returns the response
    """
    try:
        print(f"DEBUG: send_message called with session_id={request.session_id}, message={request.message[:50]}")
        
        # Get orchestrator (lazy-loaded)
        orch = get_orchestrator()
        
        # Get or create chat session
        chat_session = ChatSessionRepository.get_by_session_id(db, request.session_id)
        
        if not chat_session:
            raise HTTPException(status_code=404, detail="Chat session not found")
        
        # Convert stored messages to dict format for orchestrator
        conversation_history = []
        if chat_session.messages:
            print(f"DEBUG: chat_session.messages type={type(chat_session.messages)}, length={len(chat_session.messages)}")
            
            # Ensure messages is a list
            messages = chat_session.messages if isinstance(chat_session.messages, list) else []
            
            for i, msg in enumerate(messages):
                try:
                    if isinstance(msg, dict):
                        conversation_history.append({
                            "role": msg.get("role", "user"),
                            "content": msg.get("content", "")
                        })
                    else:
                        print(f"DEBUG: Skipping message {i} - not a dict: {type(msg)}")
                except Exception as e:
                    print(f"DEBUG: Error processing message {i}: {e}")
        
        print(f"DEBUG: conversation_history length={len(conversation_history)}")
        
        # Process message through orchestrator
        print(f"DEBUG: Calling orchestrator.process_message...")
        orchestrator_result = orch.process_message(
            request.session_id,
            request.message,
            conversation_history
        )
        print(f"DEBUG: orchestrator.process_message returned successfully")
        
        # Add user message to conversation
        user_message = {
            "role": "user",
            "content": request.message,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Add assistant response to conversation
        assistant_message = {
            "role": "assistant",
            "content": orchestrator_result["response"],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Update chat session in database
        updated_messages = (chat_session.messages or []) + [user_message, assistant_message]
        
        # Get job info from orchestrator's current session
        job_info = {}
        if (orch.current_session and 
            orch.current_session.get("session_id") == request.session_id):
            job_info = orch.current_session.get("job_info", {})
        
        update_data = {
            "messages": updated_messages,
            "is_complete": 1 if orchestrator_result["is_complete"] else 0,
            "job_info": job_info
        }
        
        # If job post was created, save it
        job_post_data = None
        if orchestrator_result.get("job_post"):
            job_post_data = orchestrator_result["job_post"]
            # Convert Pydantic model to dict if needed
            if hasattr(job_post_data, 'model_dump'):
                job_post_data = job_post_data.model_dump()
            elif hasattr(job_post_data, 'dict'):
                job_post_data = job_post_data.dict()
            update_data["job_info"] = job_post_data
        
        ChatSessionRepository.update(db, request.session_id, update_data)
        
        # If interview is complete and job post was created, save it to database
        if orchestrator_result["is_complete"] and job_post_data:
            # Create JobPost in database
            job_post_db = JobPostRepository.create(db, {
                "title": job_post_data.get("title"),
                "company": job_post_data.get("company"),
                "location": job_post_data.get("location"),
                "workplace_type": job_post_data.get("workplace_type"),
                "job_type": job_post_data.get("job_type"),
                "summary": job_post_data.get("summary"),
                "culture_and_team": job_post_data.get("culture_and_team"),
                "responsibilities": job_post_data.get("responsibilities", []),
                "requirements": job_post_data.get("requirements", []),
                "skills": job_post_data.get("skills", []),
                "keywords": job_post_data.get("keywords", []),
                "hashtags": job_post_data.get("hashtags", []),
                "tone_type": job_post_data.get("tone_type"),
                "user_id": chat_session.user_id
            })
            
            # Link job post to chat session
            ChatSessionRepository.update(db, request.session_id, {"job_post_id": job_post_db.id})
        
        return {
            "session_id": request.session_id,
            "response": orchestrator_result["response"],
            "is_complete": orchestrator_result["is_complete"],
            "job_post": job_post_data
        }
    
    except Exception as e:
        print(f"ERROR in send_message: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/post-preview/{session_id}", response_model=PostPreviewResponse)
async def get_post_preview(session_id: str, db: Session = Depends(get_db)):
    """
    Returns the current live-generated post
    """
    # Get orchestrator (lazy-loaded)
    orch = get_orchestrator()
    
    # Get chat session
    chat_session = ChatSessionRepository.get_by_session_id(db, session_id)
    
    if not chat_session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    
    # Get job post if it exists
    job_post = None
    if chat_session.job_post_id:
        job_post_db = JobPostRepository.get_by_id(db, chat_session.job_post_id)
        if job_post_db:
            job_post = db_to_pydantic_job_post(job_post_db)
    
    # If no job post in database, check if there's one in the orchestrator session
    if not job_post:
        # Try to get from orchestrator's current session
        if (orch.current_session and 
            orch.current_session.get("session_id") == session_id and
            orch.current_session.get("job_post")):
            job_post_pydantic = orch.current_session["job_post"]
            if hasattr(job_post_pydantic, 'model_dump'):
                job_post = JobPost(**job_post_pydantic.model_dump())
            elif hasattr(job_post_pydantic, 'dict'):
                job_post = JobPost(**job_post_pydantic.dict())
            else:
                job_post = JobPost(**job_post_pydantic)
    
    # If still no job post, return empty structure
    if not job_post:
        job_post = JobPost(
            responsibilities=[],
            requirements=[],
            skills=[],
            keywords=[],
            hashtags=[]
        )
    
    return PostPreviewResponse(
        session_id=session_id,
        job_post=job_post,
        is_complete=bool(chat_session.is_complete)
    )


@router.post("/save-post")
async def save_post(request: SavePostRequest, db: Session = Depends(get_db)):
    """
    Saves the post to the dashboard
    """
    # Get chat session
    chat_session = ChatSessionRepository.get_by_session_id(db, request.session_id)
    
    if not chat_session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    
    # Get job post from session
    if not chat_session.job_post_id:
        raise HTTPException(status_code=400, detail="No job post found in this session")
    
    job_post_db = JobPostRepository.get_by_id(db, chat_session.job_post_id)
    
    if not job_post_db:
        raise HTTPException(status_code=404, detail="Job post not found")
    
    # Update user_id if needed
    if job_post_db.user_id != request.user_id:
        JobPostRepository.update(db, job_post_db.id, {"user_id": request.user_id})
    
    job_post = db_to_pydantic_job_post(job_post_db)
    
    return {
        "message": "Post saved successfully",
        "job_post": job_post
    }


@router.get("/posts")
async def get_posts(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Shows saved posts for the user
    """
    job_posts = JobPostRepository.get_by_user(db, user_id, skip=skip, limit=limit)
    
    return {
        "posts": [db_to_pydantic_job_post(post) for post in job_posts],
        "total": len(job_posts)
    }


@router.post("/regenerate-section")
async def regenerate_section(request: RegenerateSectionRequest, db: Session = Depends(get_db)):
    """
    Regenerates any section:
    - Responsibilities
    - Skills
    - Summary
    - Hashtags
    - Keywords
    """
    # Get orchestrator (lazy-loaded)
    orch = get_orchestrator()
    
    # Get chat session
    chat_session = ChatSessionRepository.get_by_session_id(db, request.session_id)
    
    if not chat_session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    
    # Get job post
    if not chat_session.job_post_id:
        raise HTTPException(status_code=400, detail="No job post found in this session")
    
    job_post_db = JobPostRepository.get_by_id(db, chat_session.job_post_id)
    
    if not job_post_db:
        raise HTTPException(status_code=404, detail="Job post not found")
    
    # Convert to Pydantic model
    job_post = db_to_pydantic_job_post(job_post_db)
    
    # Regenerate section using orchestrator
    regenerated_post = orch.regenerate_section(
        request.session_id,
        request.section_type,
        job_post
    )
    
    # Update job post in database
    update_data = {
        "title": regenerated_post.title,
        "summary": regenerated_post.summary,
        "responsibilities": regenerated_post.responsibilities,
        "requirements": regenerated_post.requirements,
        "skills": regenerated_post.skills,
        "keywords": regenerated_post.keywords,
        "hashtags": regenerated_post.hashtags,
        "tone_type": regenerated_post.tone_type
    }
    
    updated_post = JobPostRepository.update(db, job_post_db.id, update_data)
    
    return {
        "message": f"Section '{request.section_type}' regenerated successfully",
        "job_post": db_to_pydantic_job_post(updated_post)
    }

