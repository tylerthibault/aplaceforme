from datetime import datetime
from src import db
from typing import Optional
import base64


class BlogPost(db.Model):
    """
    Blog post model with draft/publish functionality and scheduling.
    
    Supports rich text content, image attachments, and scheduled publishing.
    """
    __tablename__ = 'blog_posts'
    
    # Required fields
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Optional fields
    image_data = db.Column(db.LargeBinary)  # Store image as BLOB
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = db.Column(db.String(20), default='draft')  # draft, published
    publish_at = db.Column(db.DateTime)
    is_published = db.Column(db.Boolean, default=False)
    
    def publish(self) -> None:
        """
        Publish the blog post immediately.
        """
        self.is_published = True
        self.status = 'published'
        self.publish_at = datetime.utcnow()
    
    def schedule_publish(self, publish_date: datetime) -> None:
        """
        Schedule the blog post for future publication.
        
        Args:
            publish_date (datetime): When to publish the post
        """
        self.publish_at = publish_date
        self.status = 'scheduled'
    
    def unpublish(self) -> None:
        """
        Unpublish the blog post (revert to draft).
        """
        self.is_published = False
        self.status = 'draft'
        self.publish_at = None
    
    def is_scheduled(self) -> bool:
        """
        Check if post is scheduled for future publication.
        
        Returns:
            bool: True if scheduled, False otherwise
        """
        return self.publish_at and self.publish_at > datetime.utcnow()
    
    def should_be_published(self) -> bool:
        """
        Check if scheduled post should now be published.
        
        Returns:
            bool: True if it's time to publish, False otherwise
        """
        return (self.publish_at and 
                self.publish_at <= datetime.utcnow() and 
                not self.is_published)
    
    def get_excerpt(self, length: int = 150) -> str:
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
    
    def get_base64_image_data(self) -> Optional[str]:
        """
        Convert the binary image data to a Base64-encoded string.

        Returns:
            Optional[str]: Base64-encoded string of the image data, or None if no data exists.
        """
        if not self.image_data:
            return None
        return base64.b64encode(self.image_data).decode('utf-8')
    
    def __repr__(self) -> str:
        return f'<BlogPost {self.title}>'
