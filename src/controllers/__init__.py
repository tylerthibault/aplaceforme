"""
Controller package initialization.
Registers all blueprints for the application.
"""

from .main import main_bp
from .auth import auth_bp
from .admin import admin_bp
from .blog_posts import blog_posts_bp
from .god_stories import god_stories_bp
from .songs import songs_bp
from .radio_sessions import radio_sessions_bp
from .testimonials import testimonials_bp
from .users import users_bp


def register_blueprints(app):
    """Register all application blueprints."""
    # Main blueprint (public pages and media serving)
    app.register_blueprint(main_bp)
    
    # Auth blueprint (login, register, profile)
    app.register_blueprint(auth_bp)
    
    # Admin blueprint (general admin functionality)
    app.register_blueprint(admin_bp)
    
    # Model-specific admin blueprints
    app.register_blueprint(blog_posts_bp)
    app.register_blueprint(god_stories_bp)
    app.register_blueprint(songs_bp)
    app.register_blueprint(radio_sessions_bp)
    app.register_blueprint(testimonials_bp)
    app.register_blueprint(users_bp)


__all__ = [
    'main_bp',
    'auth_bp', 
    'admin_bp',
    'blog_posts_bp',
    'god_stories_bp',
    'songs_bp',
    'radio_sessions_bp',
    'testimonials_bp',
    'users_bp',
    'register_blueprints'
]
