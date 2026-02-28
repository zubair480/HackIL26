from flask import Blueprint

def register_blueprints(app):
    """Register all route blueprints with the Flask app"""
    from .auth import auth_bp
    from .location import location_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(location_bp)
