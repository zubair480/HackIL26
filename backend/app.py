"""
Flask Application Factory and Entry Point

This module creates and configures the Flask application.
"""

from flask import Flask, jsonify
from flask_cors import CORS
from config import get_config
from models.user import db
from routes import register_blueprints


def create_app(config=None):
    """
    Application factory function
    
    Args:
        config: Optional configuration object. If not provided, uses get_config()
    
    Returns:
        Configured Flask application instance
    """
    
    # Create Flask app instance
    app = Flask(__name__)
    
    # Load configuration
    if config is None:
        config = get_config()
    app.config.from_object(config)
    
    # Initialize CORS
    CORS(app)
    
    # Initialize database
    db.init_app(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register blueprints (routes)
    register_blueprints(app)
    
    # Register health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health():
        """Health check endpoint"""
        return jsonify({
            'status': 'success',
            'message': 'Backend is running'
        }), 200
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app


def register_error_handlers(app):
    """Register global error handlers"""
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'status': 'error',
            'message': 'Endpoint not found'
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'status': 'error',
            'message': 'Method not allowed'
        }), 405
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'status': 'error',
            'message': 'Internal server error'
        }), 500


def main():
    """Entry point for running the application"""
    app = create_app()
    app.run(debug=True, host='localhost', port=3000, use_reloader=False)


if __name__ == '__main__':
    main()
