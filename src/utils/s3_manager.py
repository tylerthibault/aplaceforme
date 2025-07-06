import os
from minio import Minio
from minio.error import S3Error
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class S3Manager:
    """
    Local S3 storage manager using MinIO for development.
    Can be easily switched to AWS S3 for production.
    """
    
    def __init__(self, app=None):
        self.app = app
        self.client = None
        self.boto3_client = None
        self.bucket_name = None
        self.endpoint_url = None
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize S3 manager with Flask app"""
        self.app = app
        
        # Get S3 configuration from app config
        self.endpoint_url = app.config.get('S3_ENDPOINT_URL', 'http://localhost:4566')
        self.access_key = app.config.get('S3_ACCESS_KEY', 'test')
        self.secret_key = app.config.get('S3_SECRET_KEY', 'test')
        self.bucket_name = app.config.get('S3_BUCKET_NAME', 'aplaceforme-media')
        self.region = app.config.get('S3_REGION', 'us-east-1')
        
        # Initialize MinIO client
        try:
            # Remove http:// or https:// from endpoint for MinIO client
            endpoint = self.endpoint_url.replace('http://', '').replace('https://', '')
            self.client = Minio(
                endpoint,
                access_key=self.access_key,
                secret_key=self.secret_key,
                secure=False  # Set to True for HTTPS
            )
            
            # Initialize boto3 client for S3-compatible operations
            self.boto3_client = boto3.client(
                's3',
                endpoint_url=self.endpoint_url,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                region_name=self.region
            )
            
            # Create bucket if it doesn't exist
            self._create_bucket_if_not_exists()
            
            logger.info(f"S3 Manager initialized with endpoint: {self.endpoint_url}")
            
        except Exception as e:
            logger.error(f"Failed to initialize S3 Manager: {e}")
            raise
    
    def _create_bucket_if_not_exists(self):
        """Create the bucket if it doesn't exist"""
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                logger.info(f"Created bucket: {self.bucket_name}")
            else:
                logger.info(f"Bucket {self.bucket_name} already exists")
        except S3Error as e:
            logger.error(f"Error creating/checking bucket: {e}")
            raise
    
    def upload_file(self, file_obj, folder, filename=None, content_type=None):
        """
        Upload a file to S3
        
        Args:
            file_obj: File object to upload
            folder: Folder/prefix in the bucket (e.g., 'songs', 'radio_sessions')
            filename: Optional filename override
            content_type: Optional content type override
        
        Returns:
            tuple: (success: bool, file_path: str, error_message: str)
        """
        try:
            # Generate secure filename
            if filename is None:
                filename = secure_filename(file_obj.filename)
            
            # Generate unique filename to avoid conflicts
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            unique_id = str(uuid.uuid4())[:8]
            name, ext = os.path.splitext(filename)
            unique_filename = f"{name}_{timestamp}_{unique_id}{ext}"
            
            # Full S3 key (path)
            s3_key = f"{folder}/{unique_filename}"
            
            # Get file size
            file_obj.seek(0, 2)  # Seek to end
            file_size = file_obj.tell()
            file_obj.seek(0)  # Seek back to beginning
            
            # Determine content type
            if content_type is None:
                content_type = self._get_content_type(filename)
            
            # Upload file
            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=s3_key,
                data=file_obj,
                length=file_size,
                content_type=content_type
            )
            
            # Generate URL for the uploaded file
            file_url = f"{self.endpoint_url}/{self.bucket_name}/{s3_key}"
            
            logger.info(f"Successfully uploaded file: {s3_key}")
            return True, file_url, None
            
        except S3Error as e:
            error_msg = f"S3 upload error: {e}"
            logger.error(error_msg)
            return False, None, error_msg
        except Exception as e:
            error_msg = f"Upload error: {e}"
            logger.error(error_msg)
            return False, None, error_msg
    
    def delete_file(self, file_path):
        """
        Delete a file from S3
        
        Args:
            file_path: Full URL or S3 key of the file to delete
        
        Returns:
            tuple: (success: bool, error_message: str)
        """
        try:
            # Extract S3 key from URL if needed
            if file_path.startswith('http'):
                s3_key = file_path.split(f'/{self.bucket_name}/')[-1]
            else:
                s3_key = file_path
            
            self.client.remove_object(self.bucket_name, s3_key)
            logger.info(f"Successfully deleted file: {s3_key}")
            return True, None
            
        except S3Error as e:
            error_msg = f"S3 delete error: {e}"
            logger.error(error_msg)
            return False, error_msg
        except Exception as e:
            error_msg = f"Delete error: {e}"
            logger.error(error_msg)
            return False, error_msg
    
    def get_file_url(self, s3_key, expires_in=3600):
        """
        Generate a presigned URL for a file
        
        Args:
            s3_key: S3 key of the file
            expires_in: URL expiration time in seconds
        
        Returns:
            str: Presigned URL or None if error
        """
        try:
            url = self.client.presigned_get_object(
                self.bucket_name, 
                s3_key, 
                expires=expires_in
            )
            return url
        except S3Error as e:
            logger.error(f"Error generating presigned URL: {e}")
            return None
    
    def list_files(self, folder="", limit=100):
        """
        List files in a folder
        
        Args:
            folder: Folder/prefix to list
            limit: Maximum number of files to return
        
        Returns:
            list: List of file objects
        """
        try:
            objects = self.client.list_objects(
                self.bucket_name, 
                prefix=folder,
                recursive=True
            )
            
            files = []
            for obj in objects:
                if len(files) >= limit:
                    break
                files.append({
                    'key': obj.object_name,
                    'size': obj.size,
                    'last_modified': obj.last_modified,
                    'url': f"{self.endpoint_url}/{self.bucket_name}/{obj.object_name}"
                })
            
            return files
            
        except S3Error as e:
            logger.error(f"Error listing files: {e}")
            return []
    
    def _get_content_type(self, filename):
        """Get content type based on file extension"""
        ext = os.path.splitext(filename)[1].lower()
        
        content_types = {
            # Images
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp',
            
            # Audio
            '.mp3': 'audio/mpeg',
            '.wav': 'audio/wav',
            '.ogg': 'audio/ogg',
            '.m4a': 'audio/mp4',
            
            # Video
            '.mp4': 'video/mp4',
            '.webm': 'video/webm',
            '.mov': 'video/quicktime',
            '.avi': 'video/x-msvideo',
            
            # Documents
            '.pdf': 'application/pdf',
            '.txt': 'text/plain',
        }
        
        return content_types.get(ext, 'application/octet-stream')
    
    def health_check(self):
        """Check if S3 service is healthy"""
        try:
            self.client.bucket_exists(self.bucket_name)
            return True
        except:
            return False


# Convenience functions for easier use
def upload_file(file_obj, folder, filename=None, content_type=None):
    """Convenience function to upload file"""
    from flask import current_app
    s3 = current_app.extensions.get('s3_manager')
    if s3:
        return s3.upload_file(file_obj, folder, filename, content_type)
    return False, None, "S3 Manager not initialized"

def delete_file(file_path):
    """Convenience function to delete file"""
    from flask import current_app
    s3 = current_app.extensions.get('s3_manager')
    if s3:
        return s3.delete_file(file_path)
    return False, "S3 Manager not initialized"

def get_file_url(s3_key, expires_in=3600):
    """Convenience function to get file URL"""
    from flask import current_app
    s3 = current_app.extensions.get('s3_manager')
    if s3:
        return s3.get_file_url(s3_key, expires_in)
    return None
