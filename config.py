"""
This module defines configuration settings for the application.
It contains the Config class, which is used to store important settings like database connection details,
secret keys, and session timeouts.
"""

import os
from dotenv import load_dotenv

# load environment vraiables from a .env file
load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY is not set")
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'sqlite:///bed_management.db'
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("DATABASE_URL is not set")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    if not JWT_SECRET_KEY:
        raise ValueError("JWT_SECRET_KEY is not set")
    SESSION_TIMEOUT_MINUTES = int(os.getenv('SESSION_TIMEOUT_MINUTES', 120))