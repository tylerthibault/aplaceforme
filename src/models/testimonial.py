from datetime import datetime
from src import db
from typing import Optional


class Testimonial(db.Model):
    """
    Testimonial model with approval workflow.
    
    Supports user-submitted testimonials with admin approval and scheduling.
    """
    __tablename__ = 'testimonials'
    
    # Required fields
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Optional fields
    is_approved = db.Column(db.Boolean, default=False)
    approved_at = db.Column(db.DateTime)
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    image_path = db.Column(db.String(200))
    
    # Publishing and scheduling
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = db.Column(db.String(20), default='draft')  # draft, published, scheduled
    publish_at = db.Column(db.DateTime)
    is_published = db.Column(db.Boolean, default=False)
    
    # Relationships
    approver = db.relationship('User', foreign_keys=[approved_by], backref='approved_testimonials')
    
    def approve(self, approver_id: int) -> None:
        """
        Approve the testimonial.
        
        Args:
            approver_id (int): ID of the user approving the testimonial
        """
        self.is_approved = True
        self.approved_at = datetime.utcnow()
        self.approved_by = approver_id
    
    def unapprove(self) -> None:
        """
        Remove approval from the testimonial.
        """
        self.is_approved = False
        self.approved_at = None
        self.approved_by = None
    
    def publish(self) -> None:
        """
        Publish the testimonial immediately (requires approval).
        """
        if not self.is_approved:
            raise ValueError("Testimonial must be approved before publishing")
        
        self.is_published = True
        self.status = 'published'
        self.publish_at = datetime.utcnow()
    
    def schedule_publish(self, publish_date: datetime) -> None:
        """
        Schedule the testimonial for future publication (requires approval).
        
        Args:
            publish_date (datetime): When to publish the testimonial
        """
        if not self.is_approved:
            raise ValueError("Testimonial must be approved before scheduling")
        
        self.publish_at = publish_date
        self.status = 'scheduled'
    
    def unpublish(self) -> None:
        """
        Unpublish the testimonial (revert to draft).
        """
        self.is_published = False
        self.status = 'draft'
        self.publish_at = None
    
    def should_be_published(self) -> bool:
        """
        Check if scheduled testimonial should now be published.
        
        Returns:
            bool: True if it's time to publish, False otherwise
        """
        return (self.is_approved and
                self.publish_at and 
                self.publish_at <= datetime.utcnow() and 
                not self.is_published)
    
    def is_pending_approval(self) -> bool:
        """
        Check if testimonial is pending approval.
        
        Returns:
            bool: True if pending approval, False otherwise
        """
        return not self.is_approved and self.status == 'draft'
    
    def has_image(self) -> bool:
        """
        Check if testimonial has an image.
        
        Returns:
            bool: True if has image, False otherwise
        """
        return bool(self.image_path)
    
    def get_excerpt(self, length: int = 100) -> str:
        """
        Get a truncated excerpt of the content.
        
        Args:
            length (int): Maximum length of excerpt
            
        Returns:
            str: Truncated content
        """
        if len(self.content) <= length:
            return self.content
        return self.content[:length] + '...'
    
    def __repr__(self) -> str:
        return f'<Testimonial {self.id}>'
