#!/usr/bin/env python3
"""Test script to verify all imports work correctly"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing imports...")

try:
    from database import get_db, init_db
    print("✓ database imported")
except Exception as e:
    print(f"✗ database import failed: {e}")

try:
    from models import StartChatRequest, SendMessageRequest
    print("✓ models imported")
except Exception as e:
    print(f"✗ models import failed: {e}")

try:
    from repositories import ChatSessionRepository
    print("✓ repositories imported")
except Exception as e:
    print(f"✗ repositories import failed: {e}")

try:
    from agents.orchestrator import AgentOrchestrator
    print("✓ agents.orchestrator imported")
except Exception as e:
    print(f"✗ agents.orchestrator import failed: {e}")

try:
    from routes import router
    print("✓ routes imported")
    print(f"✓ Router has {len(router.routes)} routes")
    for route in router.routes[:5]:
        print(f"  - {route.methods} {route.path}")
except Exception as e:
    print(f"✗ routes import failed: {e}")
    import traceback
    traceback.print_exc()

print("\nTesting main app...")
try:
    from main import app
    print("✓ main app imported")
    print(f"✓ App has {len(app.routes)} total routes")
except Exception as e:
    print(f"✗ main app import failed: {e}")
    import traceback
    traceback.print_exc()


