from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
import os
from typing import Optional, Union, Dict, Any

# Initialize Flask extensions
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()

# create app
def create_app(config: Optional[Union[Dict[str, Any], str]] = None) -> Flask:
    """
    Create and configure the Flask application.

    :param config: Configuration settings for the app.
    :return: Configured Flask app instance.
    """
    app = Flask(__name__)

    # Load configuration
    build_config_vars(app, config)

    # init blueprints
    init_blueprints(app)

    # init extensions
    init_extensions(app)

    # init database
    init_db(app)

    # init template filters
    init_template_filters(app)

    return app

# build config vars
def build_config_vars(app: Flask, config: Optional[Union[Dict[str, Any], str]] = None) -> Dict[str, Any]:
    """
    Build configuration variables for the application.

    :param app: Flask app instance.
    :param config: Configuration settings for the app.
    :return: Dictionary of configuration variables.
    """
    import config as app_config
    
    # Load all configuration from config.py
    app.config['SECRET_KEY'] = app_config.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = app_config.DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = app_config.DATABASE_TRACK_MODIFICATIONS
    app.config['DEBUG'] = getattr(app_config, 'DEBUG', True)
    app.config['MAX_CONTENT_LENGTH'] = getattr(app_config, 'MAX_CONTENT_LENGTH', 16 * 1024 * 1024)
    
    # Set upload folder path
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'uploads')
    
    # Override with custom config if provided
    if isinstance(config, dict):
        for key, value in config.items():
            app.config[key.upper()] = value
    elif isinstance(config, str):
        app.config['ENV'] = config
    
    # Build return dictionary of APP_ prefixed variables
    config_vars = {}
    for key, value in app.config.items():
        if key.startswith("APP_"):
            config_vars[key] = value
    
    print(f"📋 Configuration loaded successfully")
    print(f"📁 Database URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
    print(f"🔧 Debug mode: {app.config.get('DEBUG')}")
    
    return config_vars

# init blueprints
def init_blueprints(app: Flask) -> None:
    """
    Initialize and register blueprints.

    :param app: Flask app instance.
    """
    from src.controllers.main import main_bp
    from src.controllers.auth import auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

# init extensions
def init_extensions(app: Flask) -> None:
    """
    Initialize Flask extensions.

    :param app: Flask app instance.
    """
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    # Set the login view for Flask-Login
    import config as app_config
    login_manager.login_view = getattr(app_config, 'LOGIN_VIEW', 'main.login')
    login_manager.login_message_category = getattr(app_config, 'LOGIN_MESSAGE_CATEGORY', 'info')
    
    # User loader function for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        """
        Load user by ID for Flask-Login.
        
        Args:
            user_id (str): User ID
            
        Returns:
            User: User object or None
        """
        from src.models import User
        return User.query.get(int(user_id))

# init database
def init_db(app: Flask) -> None:
    """
    Initialize the database.

    :param app: Flask app instance.
    """
    with app.app_context():
        db.create_all()

# init template filters
def init_template_filters(app: Flask) -> None:
    """
    Initialize custom template filters.

    :param app: Flask app instance.
    """
    @app.template_filter('nl2br')
    def nl2br_filter(text):
        """
        Convert newlines to HTML line breaks.
        
        Args:
            text (str): Input text
            
        Returns:
            str: Text with newlines converted to <br> tags
        """
        if not text:
            return text
        return text.replace('\n', '<br>\n')

# init logger

# init mail

