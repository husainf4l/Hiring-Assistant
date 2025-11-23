#!/usr/bin/env python3
"""Test script to verify routes are importable and registered correctly"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing route imports...")
try:
    from routes import router
    print(f"✓ Routes imported successfully")
    print(f"✓ Router has {len(router.routes)} routes")
    print("\nRegistered routes:")
    for route in router.routes:
        methods = list(route.methods) if hasattr(route, 'methods') else ['?']
        path = route.path if hasattr(route, 'path') else '?'
        print(f"  {methods} {path}")
except Exception as e:
    print(f"✗ Routes import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nTesting app initialization...")
try:
    from main import app
    print(f"✓ App initialized successfully")
    print(f"✓ App has {len(app.routes)} total routes")
    api_routes = [r for r in app.routes if '/api' in str(r.path)]
    print(f"✓ App has {len(api_routes)} API routes")
    print("\nAPI routes in app:")
    for route in api_routes[:5]:
        methods = list(route.methods) if hasattr(route, 'methods') else ['?']
        path = route.path if hasattr(route, 'path') else '?'
        print(f"  {methods} {path}")
except Exception as e:
    print(f"✗ App initialization failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✓ All tests passed!")

