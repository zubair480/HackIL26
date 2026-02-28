# Code Organization Guide

Your codebase has been reorganized into a professional, modular Flask structure. Here's what you need to know:

## Quick Start

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run the Server
```bash
python app.py
```

Server starts on: `http://localhost:5000`

### Test the API
```bash
python test_api.py
```

## Project Structure

```
├── app.py                 # Main entry point (app factory)
├── wsgi.py               # Production entry point
├── config.py             # Configuration management
├── decorators.py         # Custom decorators (@token_required)
├── models/               # Database models
│   └── user.py           # User model
├── routes/               # API blueprints
│   ├── auth.py           # Authentication endpoints
│   └── location.py       # Location verification endpoints
└── [documentation files]
```

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for detailed information about each file.

## What Changed?

The original 342-line `app.py` has been split into:

- **app.py** (80 lines) - Application factory
- **models/user.py** - User model
- **routes/auth.py** - Authentication routes
- **routes/location.py** - Location routes
- **decorators.py** - Decorators
- **config.py** - Configuration

**Benefits:**
- ✅ Easier to navigate
- ✅ Easier to test
- ✅ Easier to extend
- ✅ Professional structure
- ✅ Production-ready

## Running in Production

With Gunicorn (4 workers):
```bash
gunicorn wsgi:app -w 4 -b 0.0.0.0:5000
```

## API Endpoints

All endpoints work the same as before:

- `POST /api/auth/signup` - Create account
- `POST /api/auth/login` - Login
- `GET /api/auth/profile` - Get profile (requires token)
- `POST /api/auth/logout` - Logout (requires token)
- `POST /api/location/verify` - Verify location (requires token)
- `GET /api/location/history` - Get location history (requires token)

See [README.md](README.md) for complete API documentation.

## Key Files

### app.py
The application factory - creates and configures the Flask app. Clean and simple.

### models/user.py
Database model for users. Import with:
```python
from models.user import User, db
```

### routes/auth.py & routes/location.py
Route handlers organized in Blueprint modules. Each route file contains related endpoints.

### decorators.py
Contains helpers like `@token_required`. Import with:
```python
from decorators import token_required
```

### config.py
Configuration for dev/prod/test environments. Uses environment variables.

### wsgi.py
Entry point for production WSGI servers like Gunicorn.

## Next: Deploy to Production

1. Change environment to production:
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-very-secret-key-here
   export DATABASE_URL=postgresql://user:pass@host/db
   ```

2. Install gunicorn:
   ```bash
   pip install gunicorn
   ```

3. Run with Gunicorn:
   ```bash
   gunicorn wsgi:app -w 4
   ```

4. Set up reverse proxy (Nginx/Apache) in front of Gunicorn

See [QUICK_START.md](QUICK_START.md) for more details.

---

**Everything is organized and ready to go!** 🚀