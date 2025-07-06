from datetime import datetime
from src import db
from typing import Optional


class LogEntry(db.Model):
    """
    Custom logging model for application audit trail.
    
    Stores application logs for auditing and debugging purposes.
    """
    __tablename__ = 'log_entries'
    
    # Required fields
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    level = db.Column(db.String(20), nullable=False)  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    message = db.Column(db.Text, nullable=False)
    source = db.Column(db.String(100), nullable=False)  # Module/function that generated the log
    
    # Optional fields
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    session_id = db.Column(db.String(100))
    ip_address = db.Column(db.String(45))  # IPv4 or IPv6
    user_agent = db.Column(db.String(500))
    extra_data = db.Column(db.Text)  # JSON string for additional context
    
    # Request context
    request_method = db.Column(db.String(10))  # GET, POST, etc.
    request_path = db.Column(db.String(500))
    request_params = db.Column(db.Text)  # JSON string of parameters
    
    def is_error(self) -> bool:
        """
        Check if log entry is an error level.
        
        Returns:
            bool: True if ERROR or CRITICAL level
        """
        return self.level in ['ERROR', 'CRITICAL']
    
    def is_warning(self) -> bool:
        """
        Check if log entry is a warning level.
        
        Returns:
            bool: True if WARNING level
        """
        return self.level == 'WARNING'
    
    def is_info(self) -> bool:
        """
        Check if log entry is an info level.
        
        Returns:
            bool: True if INFO level
        """
        return self.level == 'INFO'
    
    def is_debug(self) -> bool:
        """
        Check if log entry is a debug level.
        
        Returns:
            bool: True if DEBUG level
        """
        return self.level == 'DEBUG'
    
    def get_formatted_timestamp(self) -> str:
        """
        Get formatted timestamp string.
        
        Returns:
            str: Formatted timestamp
        """
        return self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    
    def get_short_message(self, length: int = 100) -> str:
        """
        Get truncated message for display.
        
        Args:
            length (int): Maximum length of message
            
        Returns:
            str: Truncated message
        """
        if len(self.message) <= length:
            return self.message
        return self.message[:length] + '...'
    
    def has_user_context(self) -> bool:
        """
        Check if log entry has user context.
        
        Returns:
            bool: True if associated with a user
        """
        return bool(self.user_id)
    
    def has_request_context(self) -> bool:
        """
        Check if log entry has request context.
        
        Returns:
            bool: True if has request information
        """
        return bool(self.request_method and self.request_path)
    
    @staticmethod
    def log_error(message: str, source: str, user_id: Optional[int] = None, 
                  extra_data: Optional[str] = None) -> 'LogEntry':
        """
        Create an error log entry.
        
        Args:
            message (str): Error message
            source (str): Source of the error
            user_id (int, optional): User ID if applicable
            extra_data (str, optional): Additional data as JSON string
            
        Returns:
            LogEntry: Created log entry
        """
        entry = LogEntry(
            level='ERROR',
            message=message,
            source=source,
            user_id=user_id,
            extra_data=extra_data
        )
        db.session.add(entry)
        return entry
    
    @staticmethod
    def log_info(message: str, source: str, user_id: Optional[int] = None,
                 extra_data: Optional[str] = None) -> 'LogEntry':
        """
        Create an info log entry.
        
        Args:
            message (str): Info message
            source (str): Source of the log
            user_id (int, optional): User ID if applicable
            extra_data (str, optional): Additional data as JSON string
            
        Returns:
            LogEntry: Created log entry
        """
        entry = LogEntry(
            level='INFO',
            message=message,
            source=source,
            user_id=user_id,
            extra_data=extra_data
        )
        db.session.add(entry)
        return entry
    
    @staticmethod
    def log_warning(message: str, source: str, user_id: Optional[int] = None,
                    extra_data: Optional[str] = None) -> 'LogEntry':
        """
        Create a warning log entry.
        
        Args:
            message (str): Warning message
            source (str): Source of the warning
            user_id (int, optional): User ID if applicable
            extra_data (str, optional): Additional data as JSON string
            
        Returns:
            LogEntry: Created log entry
        """
        entry = LogEntry(
            level='WARNING',
            message=message,
            source=source,
            user_id=user_id,
            extra_data=extra_data
        )
        db.session.add(entry)
        return entry
    
    @staticmethod
    def cleanup_old_logs(days: int = 30) -> int:
        """
        Remove old log entries.
        
        Args:
            days (int): Number of days to keep
            
        Returns:
            int: Number of entries removed
        """
        from datetime import timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        old_entries = LogEntry.query.filter(
            LogEntry.timestamp < cutoff_date
        ).all()
        
        count = len(old_entries)
        for entry in old_entries:
            db.session.delete(entry)
        
        db.session.commit()
        return count
    
    def __repr__(self) -> str:
        return f'<LogEntry {self.level}: {self.get_short_message(50)}>'
