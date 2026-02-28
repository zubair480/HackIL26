# Project Structure

## Directory Layout

```
hackillinois/
│
├── app.py                          # Flask app factory - MAIN ENTRY POINT
├── wsgi.py                         # WSGI entry point for production
├── config.py                       # Configuration management
├── requirements.txt                # Python dependencies
├── test_api.py                     # API testing script
├── decorators.py                   # Custom decorators (token_required)
├── .env.example                    # Environment variables template
│
├── models/                         # Database models
│   ├── __init__.py
│   └── user.py                     # User model
│
├── routes/                         # API route handlers
│   ├── __init__.py                 # Blueprint registration
│   ├── auth.py                     # Authentication routes
│   └── location.py                 # Location verification routes
│
├── documentation/
│   ├── README.md                   # Full API documentation
│   ├── QUICK_START.md              # Quick start guide
│   ├── FLUTTER_INTEGRATION.md      # Flutter integration examples
│   └── LOCATION_API.md             # Location API documentation
│
└── users.db                        # SQLite database (auto-created)
```

## File Responsibilities

### Core Application
- **app.py**: Flask application factory, blueprint registration, error handlers
- **config.py**: Configuration for different environments (dev, prod, test)
- **wsgi.py**: Production WSGI entry point for Gunicorn/uWSGI

### Models
- **models/user.py**: User database model with password hashing and authentication methods
- **models/__init__.py**: Model exports

### Routes (Blueprints)
- **routes/auth.py**: Signup, login, profile, logout endpoints
- **routes/location.py**: Location verification and history endpoints
- **routes/__init__.py**: Blueprint registration and initialization

### Utilities
- **decorators.py**: `token_required` decorator for protecting routes

### Configuration
- **config.py**: Environment-based configuration management
- **.env.example**: Environment variables template

## Running the Application

### Development
```bash
python app.py
```

### Production (with Gunicorn)
```bash
gunicorn wsgi:app -w 4 -b 0.0.0.0:5000
```

### Testing
```bash
python test_api.py
```

## Import Structure

### When in `routes/auth.py`:
- `from models.user import User, db` - Import User model and database
- `from decorators import token_required` - Import authentication decorator

### When in `routes/location.py`:
- `from models.user import User, db` - Import User model and database
- `from decorators import token_required` - Import authentication decorator

### When in `app.py`:
- `from config import get_config` - Import configuration
- `from models.user import db` - Import database instance
- `from routes import register_blueprints` - Import blueprint registration function

## Database

The application uses SQLAlchemy ORM with SQLite (default). The database is automatically created when the app starts.

To reset the database during development:
```bash
rm users.db
# Restart the app
python app.py
```

For production, use PostgreSQL or MySQL by setting the `DATABASE_URL` environment variable.

## Environment Variables

See `.env.example` for all available environment variables:
- `FLASK_ENV`: development, production, or testing
- `SECRET_KEY`: JWT secret key (must be set for production)
- `DATABASE_URL`: Database connection string
- `FLASK_RUN_PORT`: Server port (default: 5000)

## Benefits of This Structure

✅ **Modular**: Each component has a single responsibility  
✅ **Scalable**: Easy to add new routes and models  
✅ **Maintainable**: Clear organization and separation of concerns  
✅ **Testable**: Each module can be tested independently  
✅ **Production-Ready**: Uses Flask blueprints and factory pattern  
✅ **IDE-Friendly**: Better autocomplete and type hints
