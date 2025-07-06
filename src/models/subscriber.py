from datetime import datetime, timedelta
from src import db
from typing import Optional


class Subscriber(db.Model):
    """
    Email subscriber model for newsletter functionality.
    
    Stores email addresses and subscription status for newsletter management.
    """
    __tablename__ = 'subscribers'
    
    # Required fields
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    subscribed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Optional fields
    name = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    unsubscribed_at = db.Column(db.DateTime)
    
    # Subscription source tracking
    source = db.Column(db.String(50), default='website')  # website, admin, import
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # If linked to a user account
    
    # Relationship to user (if subscriber is also a registered user)
    user = db.relationship('User', foreign_keys=[user_id], backref='subscriber_profile')
    
    def unsubscribe(self) -> None:
        """
        Unsubscribe the email address.
        """
        self.is_active = False
        self.unsubscribed_at = datetime.utcnow()
    
    def resubscribe(self) -> None:
        """
        Resubscribe the email address.
        """
        self.is_active = True
        self.unsubscribed_at = None
        self.subscribed_at = datetime.utcnow()  # Update subscription date
    
    def get_display_name(self) -> str:
        """
        Get display name for the subscriber.
        
        Returns:
            str: Name if available, otherwise email
        """
        return self.name if self.name else self.email
    
    def is_recent_subscriber(self, days: int = 30) -> bool:
        """
        Check if subscriber joined recently.
        
        Args:
            days (int): Number of days to consider as recent
            
        Returns:
            bool: True if subscribed within the specified days
        """
        if not self.subscribed_at:
            return False
        
        days_since_subscription = (datetime.utcnow() - self.subscribed_at).days
        return days_since_subscription <= days
    
    def get_subscription_duration(self) -> int:
        """
        Get number of days since subscription.
        
        Returns:
            int: Number of days subscribed
        """
        if not self.subscribed_at:
            return 0
        
        return (datetime.utcnow() - self.subscribed_at).days
    
    @staticmethod
    def get_active_count() -> int:
        """
        Get count of active subscribers.
        
        Returns:
            int: Number of active subscribers
        """
        return Subscriber.query.filter_by(is_active=True).count()
    
    @staticmethod
    def get_recent_subscribers(days: int = 30) -> list:
        """
        Get subscribers who joined recently.
        
        Args:
            days (int): Number of days to look back
            
        Returns:
            list: List of recent subscribers
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        return Subscriber.query.filter(
            Subscriber.subscribed_at >= cutoff_date,
            Subscriber.is_active == True
        ).order_by(Subscriber.subscribed_at.desc()).all()
    
    def __repr__(self) -> str:
        return f'<Subscriber {self.email}>'
