"""
HR Hiring Assistant - FastAPI Backend
Phase 4: Data Model Implementation
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="HR Hiring Assistant API",
    description="AI-powered hiring post generator",
    version="1.0.0"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    try:
        from database import init_db
        init_db()
        print("Database initialized")
    except Exception as e:
        print(f"Database initialization error: {e}")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "HR Hiring Assistant API",
        "status": "running",
        "phase": "5"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/debug/routes")
async def debug_routes():
    """Debug endpoint to list all registered routes"""
    routes_info = []
    for route in app.routes:
        if hasattr(route, 'methods') and hasattr(route, 'path'):
            routes_info.append({
                "path": route.path,
                "methods": list(route.methods),
                "name": getattr(route, 'name', 'unknown')
            })
    return {
        "total_routes": len(routes_info),
        "routes": routes_info
    }


# Include API routes
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from routes import router
    from job_finder.routes import router as job_finder_router

    app.include_router(router, prefix="/api", tags=["api"])
    app.include_router(job_finder_router, prefix="/api", tags=["job-finder"])
    print("✓ API routes loaded successfully")
except ImportError as e:
    print(f"ERROR: Could not import routes: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"ERROR loading routes: {e}")
    import traceback
    traceback.print_exc()

# Include Rolevate integration routes
try:
    from rolevate_routes import router as rolevate_router
    app.include_router(rolevate_router, prefix="/api", tags=["rolevate"])
    print("✓ Rolevate integration routes loaded successfully")
except ImportError as e:
    print(f"WARNING: Could not import Rolevate routes: {e}")
except Exception as e:
    print(f"WARNING: Error loading Rolevate routes: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

