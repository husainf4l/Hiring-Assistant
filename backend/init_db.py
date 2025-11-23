"""
Database initialization script
Phase 4: Data Model
Run this script to initialize the database
Usage: python -m backend.init_db
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import init_db, engine

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Database initialized successfully!")
    print(f"Database location: {engine.url}")

