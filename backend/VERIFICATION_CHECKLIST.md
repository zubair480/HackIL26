# ✅ Post-Refactoring Checklist

Use this checklist to verify the reorganized codebase is working correctly.

## Step 1: Verify File Structure

```bash
# Run this command to see the file structure
ls -la

# You should see:
# ✅ app.py
# ✅ config.py
# ✅ decorators.py
# ✅ requirements.txt
# ✅ wsgi.py
# ✅ test_api.py
# ✅ models/ (directory)
# ✅ routes/ (directory)
# ✅ Various .md documentation files
```

## Step 2: Check Models Directory

```bash
ls -la models/

# You should see:
# ✅ __init__.py
# ✅ user.py
```

## Step 3: Check Routes Directory

```bash
ls -la routes/

# You should see:
# ✅ __init__.py
# ✅ auth.py
# ✅ location.py
```

## Step 4: Verify Imports (Optional)

```bash
# Run the import verification script
python verify_organization.py

# Expected output:
# ✅ config.py - OK
# ✅ models/user.py - OK
# ✅ decorators.py - OK
# ✅ routes/auth.py - OK
# ✅ routes/location.py - OK
# ✅ app.py - OK
# ✅ create_app() - OK
# ✅ All imports successful!
```

## Step 5: Install Dependencies

```bash
pip install -r requirements.txt

# Should install:
# ✅ Flask
# ✅ Flask-SQLAlchemy
# ✅ Flask-CORS
# ✅ PyJWT
# ✅ Werkzeug
# ✅ python-dotenv
# ✅ geopy
# ✅ gunicorn
```

## Step 6: Run the Application

```bash
python app.py

# Expected output:
# ✅ * Running on http://0.0.0.0:5000
# ✅ * Debug mode: on

# Test the health check:
# curl http://localhost:5000/api/health

# Expected response:
# {"status": "success", "message": "Backend is running"}
```

## Step 7: Run API Tests

```bash
# In another terminal:
python test_api.py

# Expected output:
# ✅ Tests Passed: X/X
# ✅ All test results should show PASS
```

## Step 8: Test Key Endpoints

```bash
# Test signup
curl -X POST http://localhost:5000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"jane_test","email":"jane@test.com","password":"pass123"}'

# Should return:
# ✅ 201 status
# ✅ User data in response
# ✅ Token in response

# Test login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"jane_test","password":"pass123"}'

# Should return:
# ✅ 200 status
# ✅ Token in response

# Test location verify (replace TOKEN with actual token)
curl -X POST http://localhost:5000/api/location/verify \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "lat": 40.7580,
    "lng": -73.9855,
    "target_address": "Times Square, New York, NY"
  }'

# Should return:
# ✅ 200 status
# ✅ distance_meters in response
# ✅ productivity_status (GREEN/YELLOW/RED)
```

## Step 9: Verify Database

```bash
# Check if database was created
ls -la *.db

# You should see:
# ✅ users.db (SQLite database)
```

## Step 10: Check Configuration

```bash
# Verify config.py loads correctly
python -c "from config import get_config; config = get_config(); print('✅ Config loaded successfully')"

# Expected output:
# ✅ Config loaded successfully
```

## Troubleshooting

### If imports fail:
```bash
# Make sure you're in the right directory
pwd  # Should end with: hackillinois

# Check Python path
python -c "import sys; print(sys.path)"

# Run the verification script
python verify_organization.py
```

### If database errors occur:
```bash
# Delete the database and restart
rm users.db
python app.py  # Will recreate the database
```

### If port is already in use:
```bash
# Change port in app.py (last line):
app.run(debug=True, host='0.0.0.0', port=5001)  # Use 5001 instead
```

### If you see "ModuleNotFoundError":
```bash
# Make sure all __init__.py files exist
ls models/__init__.py   # Should exist
ls routes/__init__.py   # Should exist

# Make sure you're in the project root
cd /path/to/hackillinois
python app.py
```

## Verification Summary

Complete this checklist:

- [ ] File structure is correct (app.py, models/, routes/, etc.)
- [ ] models/ directory has __init__.py and user.py
- [ ] routes/ directory has __init__.py, auth.py, location.py
- [ ] Import verification passes (python verify_organization.py)
- [ ] Dependencies installed (pip install -r requirements.txt)
- [ ] App runs without errors (python app.py)
- [ ] Health check works (GET /api/health)
- [ ] API tests pass (python test_api.py)
- [ ] Signup endpoint works
- [ ] Login endpoint works
- [ ] Location verification works
- [ ] Database file was created (users.db)

## Next Steps

If everything checks out:

1. ✅ Read [REFACTORING_COMPLETE.md](REFACTORING_COMPLETE.md)
2. ✅ Review [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
3. ✅ Check [ORGANIZATION_GUIDE.md](ORGANIZATION_GUIDE.md)
4. ✅ Start integrating with Flutter
5. ✅ Deploy to production using [wsgi.py](wsgi.py)

---

**Congratulations! Your codebase is now professionally organized.** 🎉
