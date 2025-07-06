from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from src import db
from typing import Optional


class User(UserMixin, db.Model):
    """
    User model for storing user accounts (admin, subscribers, regular users, authors).
    
    Supports different roles and tracks if user is admin-managed or self-registered.
    """
    __tablename__ = 'users'
    
    # Required fields
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')  # admin, user, author
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Optional fields
    last_login = db.Column(db.DateTime)
    is_managed = db.Column(db.Boolean, default=False)  # True if admin-created, False if self-registered
    
    # Relationships
    blog_posts = db.relationship('BlogPost', foreign_keys='BlogPost.author_id', backref='author', lazy=True)
    god_stories = db.relationship('GodStory', foreign_keys='GodStory.author_id', backref='author', lazy=True)
    songs = db.relationship('Song', foreign_keys='Song.uploaded_by', backref='uploader', lazy=True)
    testimonials = db.relationship('Testimonial', foreign_keys='Testimonial.author_id', backref='author', lazy=True)
    newsletters = db.relationship('Newsletter', foreign_keys='Newsletter.author_id', backref='author', lazy=True)
    radio_sessions = db.relationship('RadioSession', foreign_keys='RadioSession.uploaded_by', backref='uploader', lazy=True)
    session_tokens = db.relationship('SessionToken', foreign_keys='SessionToken.user_id', backref='user', lazy=True)
    log_entries = db.relationship('LogEntry', foreign_keys='LogEntry.user_id', backref='user', lazy=True)
    
    def set_password(self, password: str) -> None:
        """
        Set password hash for the user.
        
        Args:
            password (str): Plain text password
        """
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password: str) -> bool:
        """
        Check if provided password matches the stored hash.
        
        Args:
            password (str): Plain text password to check
            
        Returns:
            bool: True if password matches, False otherwise
        """
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self) -> bool:
        """
        Check if user has admin role.
        
        Returns:
            bool: True if user is admin, False otherwise
        """
        return self.role == 'admin'
    
    def is_author(self) -> bool:
        """
        Check if user has author role.
        
        Returns:
            bool: True if user is author, False otherwise
        """
        return self.role == 'author'
    
    def update_last_login(self) -> None:
        """
        Update the last login timestamp.
        """
        self.last_login = datetime.utcnow()
    
    def __repr__(self) -> str:
        return f'<User {self.username}>'
