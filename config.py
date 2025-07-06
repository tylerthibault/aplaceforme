# APP INFORMATION
APP_NAME = "A Place For Me"
APP_DESCRIPTION = "A Place For Me is a platform that connects people with similar interests and provides a space for them to share their thoughts, ideas, and experiences."
APP_VERSION = "1.0.0"
APP_AUTHOR = "Tyler Thibault"

# APP CONFIGURATION
PORT = 5000
HOST = "0.0.0.0"
DEBUG = True  # Default to debug mode for development

# DATABASE CONFIGURATION
DATABASE_URI = "sqlite:///aplaceforme.db"  # Use SQLite for simplicity; change
# to a different database URI for production
DATABASE_TRACK_MODIFICATIONS = False  # Disable track modifications to save resources

# SECURITY CONFIGURATION
SECRET_KEY = "your_secret"

# FILE UPLOAD CONFIGURATION
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3', 'wav', 'mp4', 'mov'}

# FLASK-LOGIN CONFIGURATION
LOGIN_VIEW = 'auth.login'
LOGIN_MESSAGE_CATEGORY = 'info'

# MAIL CONFIGURATION
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = None  # Set via environment variable
MAIL_PASSWORD = None  # Set via environment variable
MAIL_DEFAULT_SENDER = 'noreply@aplaceforme.com'

# PAGINATION CONFIGURATION
POSTS_PER_PAGE = 10
ADMIN_EMAIL = 'admin@aplaceforme.com'
