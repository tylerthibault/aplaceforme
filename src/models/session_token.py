from datetime import datetime
from src import db
from typing import Optional


class SessionToken(db.Model):
    """
    Session token model for logged-in users.
    
    Stores secure session tokens for user authentication with expiration.
    """
    __tablename__ = 'session_tokens'
    
    # Required fields
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token_hash = db.Column(db.String(255), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    
    # Optional fields
    is_active = db.Column(db.Boolean, default=True)
    last_used = db.Column(db.DateTime)
    ip_address = db.Column(db.String(45))  # IPv4 or IPv6
    user_agent = db.Column(db.String(500))
    
    def is_expired(self) -> bool:
        """
        Check if the token is expired.
        
        Returns:
            bool: True if expired, False otherwise
        """
        return datetime.utcnow() > self.expires_at
    
    def is_valid(self) -> bool:
        """
        Check if the token is valid (active and not expired).
        
        Returns:
            bool: True if valid, False otherwise
        """
        return self.is_active and not self.is_expired()
    
    def deactivate(self) -> None:
        """
        Deactivate the token.
        """
        self.is_active = False
    
    def update_last_used(self) -> None:
        """
        Update the last used timestamp.
        """
        self.last_used = datetime.utcnow()
    
    def extend_expiration(self, hours: int = 24) -> None:
        """
        Extend the token expiration time.
        
        Args:
            hours (int): Number of hours to extend
        """
        from datetime import timedelta
        self.expires_at = datetime.utcnow() + timedelta(hours=hours)
    
    def get_remaining_time(self) -> int:
        """
        Get remaining time before expiration in seconds.
        
        Returns:
            int: Remaining seconds (0 if expired)
        """
        if self.is_expired():
            return 0
        
        remaining = self.expires_at - datetime.utcnow()
        return int(remaining.total_seconds())
    
    def get_age(self) -> int:
        """
        Get age of the token in seconds.
        
        Returns:
            int: Age in seconds
        """
        age = datetime.utcnow() - self.created_at
        return int(age.total_seconds())
    
    @staticmethod
    def cleanup_expired() -> int:
        """
        Remove expired tokens from the database.
        
        Returns:
            int: Number of tokens removed
        """
        expired_tokens = SessionToken.query.filter(
            SessionToken.expires_at < datetime.utcnow()
        ).all()
        
        count = len(expired_tokens)
        for token in expired_tokens:
            db.session.delete(token)
        
        db.session.commit()
        return count
    
    @staticmethod
    def deactivate_user_tokens(user_id: int) -> int:
        """
        Deactivate all tokens for a specific user.
        
        Args:
            user_id (int): User ID
            
        Returns:
            int: Number of tokens deactivated
        """
        tokens = SessionToken.query.filter_by(
            user_id=user_id, 
            is_active=True
        ).all()
        
        count = len(tokens)
        for token in tokens:
            token.deactivate()
        
        db.session.commit()
        return count
    
    def __repr__(self) -> str:
        return f'<SessionToken {self.id} for User {self.user_id}>'
