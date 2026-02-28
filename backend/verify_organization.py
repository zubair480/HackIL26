#!/usr/bin/env python3
"""
Verification script to check if the code organization is correct
and all imports work without circular dependencies
"""

import sys
import traceback

def check_imports():
    """Check if all modules can be imported without errors"""
    print("🔍 Checking imports...\n")
    
    errors = []
    
    # Test 1: Import config
    try:
        from config import get_config
        print("✅ config.py - OK")
    except Exception as e:
        errors.append(f"❌ config.py - {str(e)}")
        traceback.print_exc()
    
    # Test 2: Import models
    try:
        from models.user import User, db
        print("✅ models/user.py - OK")
    except Exception as e:
        errors.append(f"❌ models/user.py - {str(e)}")
        traceback.print_exc()
    
    # Test 3: Import decorators
    try:
        from decorators import token_required
        print("✅ decorators.py - OK")
    except Exception as e:
        errors.append(f"❌ decorators.py - {str(e)}")
        traceback.print_exc()
    
    # Test 4: Import routes
    try:
        from routes.auth import auth_bp
        print("✅ routes/auth.py - OK")
    except Exception as e:
        errors.append(f"❌ routes/auth.py - {str(e)}")
        traceback.print_exc()
    
    try:
        from routes.location import location_bp
        print("✅ routes/location.py - OK")
    except Exception as e:
        errors.append(f"❌ routes/location.py - {str(e)}")
        traceback.print_exc()
    
    # Test 5: Import app factory
    try:
        from app import create_app
        print("✅ app.py - OK")
    except Exception as e:
        errors.append(f"❌ app.py - {str(e)}")
        traceback.print_exc()
    
    # Test 6: Create app instance
    try:
        from app import create_app
        from config import TestingConfig
        app = create_app(config=TestingConfig)
        print("✅ create_app() - OK")
    except Exception as e:
        errors.append(f"❌ create_app() - {str(e)}")
        traceback.print_exc()
    
    print()
    
    if errors:
        print("❌ ERRORS FOUND:\n")
        for error in errors:
            print(f"  {error}")
        return False
    else:
        print("✅ All imports successful! Your code is properly organized.")
        return True

if __name__ == '__main__':
    success = check_imports()
    sys.exit(0 if success else 1)
