"""
Flask Configuration File

Handles different configurations for development, production, and testing.
Use environment variables to control which config is loaded.
"""

import os
from datetime import timedelta


class Config:
    """Base configuration - shared across all environments"""
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///users.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
    JWT_EXPIRATION_DELTA = timedelta(days=30)
    
    # API Configuration
    JSON_SORT_KEYS = False


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    # Uses SECRET_KEY from base Config with default value
    # Override if needed: SECRET_KEY = os.getenv('SECRET_KEY')


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


# Config factory
def get_config():
    """Get configuration object based on FLASK_ENV environment variable"""
    env = os.getenv('FLASK_ENV', 'development')
    config_map = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig
    }
    return config_map.get(env, DevelopmentConfig)
