from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    """
    User model for authentication and location tracking
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_verified_location = db.Column(db.String(255), nullable=True)
    last_verified_lat = db.Column(db.Float, nullable=True)
    last_verified_lng = db.Column(db.Float, nullable=True)
    last_verification_time = db.Column(db.DateTime, nullable=True)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password hash"""
        return check_password_hash(self.password, password)
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'last_verified_location': self.last_verified_location,
            'last_verification_time': self.last_verification_time.isoformat() if self.last_verification_time else None
        }
