"""
WSGI entry point for production deployment

Use with Gunicorn:
    gunicorn wsgi:app

Or other WSGI servers (uWSGI, etc.)
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run()
