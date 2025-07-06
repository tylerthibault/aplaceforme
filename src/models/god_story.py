from datetime import datetime
from src import db
from typing import Optional


class GodStory(db.Model):
    """
    God/faith stories model with multimedia support.
    
    Supports text content, audio, video, and image attachments with scheduling.
    """
    __tablename__ = 'god_stories'
    
    # Required fields
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Optional fields - multimedia support
    audio_path = db.Column(db.String(200))
    video_path = db.Column(db.String(200))
    image_path = db.Column(db.String(200))
    
    # Publishing and scheduling
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = db.Column(db.String(20), default='draft')  # draft, published, scheduled
    publish_at = db.Column(db.DateTime)
    is_published = db.Column(db.Boolean, default=False)
    
    def publish(self) -> None:
        """
        Publish the God story immediately.
        """
        self.is_published = True
        self.status = 'published'
        self.publish_at = datetime.utcnow()
    
    def schedule_publish(self, publish_date: datetime) -> None:
        """
        Schedule the God story for future publication.
        
        Args:
            publish_date (datetime): When to publish the story
        """
        self.publish_at = publish_date
        self.status = 'scheduled'
    
    def unpublish(self) -> None:
        """
        Unpublish the God story (revert to draft).
        """
        self.is_published = False
        self.status = 'draft'
        self.publish_at = None
    
    def has_audio(self) -> bool:
        """
        Check if story has audio content.
        
        Returns:
            bool: True if has audio, False otherwise
        """
        return bool(self.audio_path)
    
    def has_video(self) -> bool:
        """
        Check if story has video content.
        
        Returns:
            bool: True if has video, False otherwise
        """
        return bool(self.video_path)
    
    def has_image(self) -> bool:
        """
        Check if story has image content.
        
        Returns:
            bool: True if has image, False otherwise
        """
        return bool(self.image_path)
    
    def is_multimedia(self) -> bool:
        """
        Check if story has any multimedia content.
        
        Returns:
            bool: True if has multimedia, False otherwise
        """
        return self.has_audio() or self.has_video() or self.has_image()
    
    def should_be_published(self) -> bool:
        """
        Check if scheduled story should now be published.
        
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
    
    def __repr__(self) -> str:
        return f'<GodStory {self.title}>'
