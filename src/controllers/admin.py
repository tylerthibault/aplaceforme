from flask import Blueprint, render_template, request, flash, redirect, url_for
from datetime import datetime
import logging
from src.models import BlogPost, GodStory, Song, Testimonial, RadioSession, User
from src import db
from flask_login import login_required, current_user

# Set up logging
logger = logging.getLogger(__name__)

# Create blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/blog-posts')
@login_required
def admin_blog_posts():
    """Display all blog posts for admin management."""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('admin/blog_posts.html', 
                         posts=posts, 
                         pagination=posts, 
                         title='Manage Blog Posts', 
                         add_url=url_for('blog_posts.new_blog_post'))


@admin_bp.route('/god-stories')
@login_required
def admin_god_stories():
    """Display all God stories for admin management."""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    stories = GodStory.query.order_by(GodStory.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('admin/god_stories.html', 
                         stories=stories, 
                         pagination=stories, 
                         title='Manage God Stories', 
                         add_url=url_for('god_stories.new_god_story'))


@admin_bp.route('/songs')
@login_required
def admin_songs():
    """Display all songs for admin management."""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    songs = Song.query.order_by(Song.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('admin/songs.html', 
                         songs=songs, 
                         pagination=songs, 
                         title='Manage Songs', 
                         add_url=url_for('songs.new_song'))


@admin_bp.route('/testimonials')
@login_required
def admin_testimonials():
    """Display all testimonials for admin management."""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    testimonials = Testimonial.query.order_by(Testimonial.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('admin/testimonials.html', 
                         testimonials=testimonials, 
                         pagination=testimonials, 
                         title='Manage Testimonials', 
                         add_url=url_for('testimonials.new_testimonial'))


@admin_bp.route('/radio-sessions')
@login_required
def admin_radio_sessions():
    """Display all radio sessions for admin management."""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    sessions = RadioSession.query.order_by(RadioSession.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('admin/radio_sessions.html', 
                         sessions=sessions, 
                         pagination=sessions, 
                         title='Manage Radio Sessions', 
                         add_url=url_for('radio_sessions.new_radio_session'))


@admin_bp.route('/users')
@login_required
def admin_users():
    """Display all users for admin management."""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    users = User.query.paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('admin/users.html', 
                         users=users, 
                         pagination=users, 
                         title='Manage Users', 
                         add_url=url_for('users.new_user'))