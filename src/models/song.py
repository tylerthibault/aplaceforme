from datetime import datetime
from src import db
from typing import Optional
import base64


class Song(db.Model):
    """
    Song model for audio file uploads.
    
    Supports music uploads with scheduling and metadata.
    """
    __tablename__ = 'songs'
    
    # Required fields
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    file_data = db.Column(db.LargeBinary, nullable=False)  # Store audio file as BLOB
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Optional fields
    description = db.Column(db.Text)
    artist = db.Column(db.String(200))
    album = db.Column(db.String(200))
    genre = db.Column(db.String(100))
    duration = db.Column(db.Integer)  # Duration in seconds
    
    # Publishing and scheduling
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = db.Column(db.String(20), default='draft')  # draft, published, scheduled
    publish_at = db.Column(db.DateTime)
    is_published = db.Column(db.Boolean, default=False)
    
    def publish(self) -> None:
        """
        Publish the song immediately.
        """
        self.is_published = True
        self.status = 'published'
        self.publish_at = datetime.utcnow()
    
    def schedule_publish(self, publish_date: datetime) -> None:
        """
        Schedule the song for future publication.
        
        Args:
            publish_date (datetime): When to publish the song
        """
        self.publish_at = publish_date
        self.status = 'scheduled'
    
    def unpublish(self) -> None:
        """
        Unpublish the song (revert to draft).
        """
        self.is_published = False
        self.status = 'draft'
        self.publish_at = None
    
    def should_be_published(self) -> bool:
        """
        Check if scheduled song should now be published.
        
        Returns:
            bool: True if it's time to publish, False otherwise
        """
        return (self.publish_at and 
                self.publish_at <= datetime.utcnow() and 
                not self.is_published)
    
    def get_formatted_duration(self) -> str:
        """
        Get formatted duration string (MM:SS).
        
        Returns:
            str: Formatted duration or 'Unknown' if not set
        """
        if not self.duration:
            return 'Unknown'
        
        minutes = self.duration // 60
        seconds = self.duration % 60
        return f"{minutes}:{seconds:02d}"
    
    def get_display_artist(self) -> str:
        """
        Get artist name or default if not set.
        
        Returns:
            str: Artist name or 'Unknown Artist'
        """
        return self.artist if self.artist else 'Unknown Artist'
    
    def get_display_album(self) -> str:
        """
        Get album name or default if not set.
        
        Returns:
            str: Album name or 'Unknown Album'
        """
        return self.album if self.album else 'Unknown Album'
    
    def get_base64_file_data(self) -> Optional[str]:
        """
        Convert the binary file data to a Base64-encoded string.

        Returns:
            Optional[str]: Base64-encoded string of the file data, or None if no data exists.
        """
        if not self.file_data:
            return None
        return base64.b64encode(self.file_data).decode('utf-8')
    
    def __repr__(self) -> str:
        return f'<Song {self.title}>'
