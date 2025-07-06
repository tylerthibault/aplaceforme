from datetime import datetime
from src import db
from typing import Optional


class Newsletter(db.Model):
    """
    Newsletter model for email campaigns.
    
    Supports draft/scheduled/sent status and tracks email campaign metadata.
    """
    __tablename__ = 'newsletters'
    
    # Required fields
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime)
    
    # Optional fields
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.String(20), default='draft')  # draft, scheduled, sent
    scheduled_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Email campaign metrics
    recipients_count = db.Column(db.Integer, default=0)
    sent_count = db.Column(db.Integer, default=0)
    failed_count = db.Column(db.Integer, default=0)
    
    def schedule(self, scheduled_date: datetime) -> None:
        """
        Schedule the newsletter for future sending.
        
        Args:
            scheduled_date (datetime): When to send the newsletter
        """
        self.scheduled_at = scheduled_date
        self.status = 'scheduled'
    
    def send(self, recipients_count: int = 0) -> None:
        """
        Mark the newsletter as sent.
        
        Args:
            recipients_count (int): Number of recipients
        """
        self.sent_at = datetime.utcnow()
        self.status = 'sent'
        self.recipients_count = recipients_count
    
    def mark_as_draft(self) -> None:
        """
        Revert newsletter to draft status.
        """
        self.status = 'draft'
        self.scheduled_at = None
        self.sent_at = None
    
    def should_be_sent(self) -> bool:
        """
        Check if scheduled newsletter should now be sent.
        
        Returns:
            bool: True if it's time to send, False otherwise
        """
        return (self.status == 'scheduled' and
                self.scheduled_at and 
                self.scheduled_at <= datetime.utcnow())
    
    def is_sent(self) -> bool:
        """
        Check if newsletter has been sent.
        
        Returns:
            bool: True if sent, False otherwise
        """
        return self.status == 'sent'
    
    def is_scheduled(self) -> bool:
        """
        Check if newsletter is scheduled.
        
        Returns:
            bool: True if scheduled, False otherwise
        """
        return self.status == 'scheduled'
    
    def get_success_rate(self) -> float:
        """
        Get the success rate of the newsletter sending.
        
        Returns:
            float: Success rate as percentage (0-100)
        """
        if self.recipients_count == 0:
            return 0.0
        
        return (self.sent_count / self.recipients_count) * 100
    
    def get_failure_rate(self) -> float:
        """
        Get the failure rate of the newsletter sending.
        
        Returns:
            float: Failure rate as percentage (0-100)
        """
        if self.recipients_count == 0:
            return 0.0
        
        return (self.failed_count / self.recipients_count) * 100
    
    def update_sending_stats(self, sent: int, failed: int) -> None:
        """
        Update sending statistics.
        
        Args:
            sent (int): Number of successfully sent emails
            failed (int): Number of failed emails
        """
        self.sent_count = sent
        self.failed_count = failed
    
    def get_preview(self, length: int = 100) -> str:
        """
        Get a preview of the newsletter body.
        
        Args:
            length (int): Maximum length of preview
            
        Returns:
            str: Truncated body content
        """
        if len(self.body) <= length:
            return self.body
        return self.body[:length] + '...'
    
    def __repr__(self) -> str:
        return f'<Newsletter {self.subject}>'
