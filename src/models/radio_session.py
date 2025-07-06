from datetime import datetime
from src import db
from typing import Optional


class RadioSession(db.Model):
    """
    Radio session model for audio/podcast uploads.
    
    Supports audio content with metadata and scheduling functionality.
    """
    __tablename__ = 'radio_sessions'
    
    # Required fields
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    file_path = db.Column(db.String(200), nullable=False)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Optional fields
    description = db.Column(db.Text)
    duration = db.Column(db.Integer)  # Duration in seconds
    episode_number = db.Column(db.Integer)
    season_number = db.Column(db.Integer)
    
    # Publishing and scheduling
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = db.Column(db.String(20), default='draft')  # draft, published, scheduled
    publish_at = db.Column(db.DateTime)
    is_published = db.Column(db.Boolean, default=False)
    
    # Metadata
    tags = db.Column(db.String(500))  # Comma-separated tags
    thumbnail_path = db.Column(db.String(200))
    download_count = db.Column(db.Integer, default=0)
    
    def publish(self) -> None:
        """
        Publish the radio session immediately.
        """
        self.is_published = True
        self.status = 'published'
        self.publish_at = datetime.utcnow()
    
    def schedule_publish(self, publish_date: datetime) -> None:
        """
        Schedule the radio session for future publication.
        
        Args:
            publish_date (datetime): When to publish the session
        """
        self.publish_at = publish_date
        self.status = 'scheduled'
    
    def unpublish(self) -> None:
        """
        Unpublish the radio session (revert to draft).
        """
        self.is_published = False
        self.status = 'draft'
        self.publish_at = None
    
    def should_be_published(self) -> bool:
        """
        Check if scheduled session should now be published.
        
        Returns:
            bool: True if it's time to publish, False otherwise
        """
        return (self.publish_at and 
                self.publish_at <= datetime.utcnow() and 
                not self.is_published)
    
    def increment_download_count(self) -> None:
        """
        Increment the download counter.
        """
        self.download_count += 1
    
    def get_formatted_duration(self) -> str:
        """
        Get formatted duration string (HH:MM:SS or MM:SS).
        
        Returns:
            str: Formatted duration or 'Unknown' if not set
        """
        if not self.duration:
            return 'Unknown'
        
        hours = self.duration // 3600
        minutes = (self.duration % 3600) // 60
        seconds = self.duration % 60
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes}:{seconds:02d}"
    
    def get_episode_title(self) -> str:
        """
        Get formatted episode title with season/episode numbers.
        
        Returns:
            str: Formatted episode title
        """
        if self.season_number and self.episode_number:
            return f"S{self.season_number}E{self.episode_number}: {self.title}"
        elif self.episode_number:
            return f"Episode {self.episode_number}: {self.title}"
        else:
            return self.title
    
    def get_tags_list(self) -> list:
        """
        Get tags as a list.
        
        Returns:
            list: List of tags
        """
        if not self.tags:
            return []
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    def set_tags(self, tags: list) -> None:
        """
        Set tags from a list.
        
        Args:
            tags (list): List of tag strings
        """
        self.tags = ', '.join(tags) if tags else None
    
    def has_thumbnail(self) -> bool:
        """
        Check if session has a thumbnail.
        
        Returns:
            bool: True if has thumbnail, False otherwise
        """
        return bool(self.thumbnail_path)
    
    def get_description_preview(self, length: int = 150) -> str:
        """
        Get a preview of the description.
        
        Args:
            length (int): Maximum length of preview
            
        Returns:
            str: Truncated description
        """
        if not self.description:
            return 'No description available'
        
        if len(self.description) <= length:
            return self.description
        return self.description[:length] + '...'
    
    def __repr__(self) -> str:
        return f'<RadioSession {self.title}>'
