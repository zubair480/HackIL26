from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import jwt
from models.user import User, db
from decorators import token_required

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/signup', methods=['POST'])
def signup():
    """
    User signup endpoint
    
    Request body:
    {
        "username": "john_doe",
        "email": "john@example.com",
        "password": "securepassword123"
    }
    """
    try:
        data = request.get_json()
        
        # Validate input
        if not data or not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify({
                'status': 'error',
                'message': 'Missing required fields: username, email, password'
            }), 400
        
        username = data.get('username').strip()
        email = data.get('email').strip()
        password = data.get('password')
        
        # Validate input length
        if len(username) < 3:
            return jsonify({
                'status': 'error',
                'message': 'Username must be at least 3 characters long'
            }), 400
        
        if len(password) < 6:
            return jsonify({
                'status': 'error',
                'message': 'Password must be at least 6 characters long'
            }), 400
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return jsonify({
                'status': 'error',
                'message': 'Username already exists'
            }), 409
        
        if User.query.filter_by(email=email).first():
            return jsonify({
                'status': 'error',
                'message': 'Email already registered'
            }), 409
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        # Generate token
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(days=30)
        }, jwt_secret_key(), algorithm='HS256')
        
        return jsonify({
            'status': 'success',
            'message': 'User created successfully',
            'token': token,
            'user': user.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User login endpoint
    
    Request body:
    {
        "username": "john_doe",
        "password": "securepassword123"
    }
    """
    try:
        data = request.get_json()
        
        # Validate input
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({
                'status': 'error',
                'message': 'Missing required fields: username, password'
            }), 400
        
        username = data.get('username').strip()
        password = data.get('password')
        
        # Find user by username or email
        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).first()
        
        if not user or not user.check_password(password):
            return jsonify({
                'status': 'error',
                'message': 'Invalid username/email or password'
            }), 401
        
        # Generate token
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(days=30)
        }, jwt_secret_key(), algorithm='HS256')
        
        return jsonify({
            'status': 'success',
            'message': 'Login successful',
            'token': token,
            'user': user.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }), 500


@auth_bp.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    """Get current user profile (protected route)"""
    return jsonify({
        'status': 'success',
        'user': current_user.to_dict()
    }), 200


@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    """Logout endpoint (token-based, just confirm logout on client side)"""
    return jsonify({
        'status': 'success',
        'message': 'Logged out successfully'
    }), 200


def jwt_secret_key():
    """Get JWT secret key from app config"""
    from flask import current_app
    return current_app.config['SECRET_KEY']
