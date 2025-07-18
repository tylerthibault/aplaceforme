from flask import Blueprint, render_template, request, abort, Response, flash, redirect, url_for
from typing import Tuple
from datetime import datetime
import logging
from src.models import BlogPost, GodStory, Song, Testimonial, RadioSession, User
from flask_login import login_required, current_user

# Set up logging
logger = logging.getLogger(__name__)

# Create main blueprint
main_bp = Blueprint('main', __name__)


def check_video_has_audio(video_data):
    """
    Check if video file contains audio tracks.
    
    Args:
        video_data: Binary video data
        
    Returns:
        bool: True if audio tracks found, False otherwise
    """
    if not video_data or len(video_data) < 100:
        return False
    
    # Convert to hex string for pattern matching
    data_hex = video_data.hex()
    
    # Check for audio track indicators in MP4/MOV files
    has_audio = any([
        'soun' in data_hex,  # Sound track
        'mp4a' in data_hex,  # MP4 audio codec
        'aac' in data_hex.lower(),   # AAC audio
        'audio' in data_hex.lower()  # Generic audio indicator
    ])
    
    return has_audio


# Public Pages
@main_bp.route('/')
def index():
    """
    Display the home page.
    
    Returns:
        Response: Home page template
    """
    # Get recent testimonials for the landing page
    testimonials = Testimonial.query.filter_by(is_published=True, is_approved=True)\
                                   .order_by(Testimonial.created_at.desc())\
                                   .limit(12).all()  # Get 12 to support show all functionality
    
    return render_template('public/landing/index.html', testimonials=testimonials)


@main_bp.route('/about')
def about():
    """
    Display the about page.
    
    Returns:
        Response: About page template
    """
    return render_template('public/about.html')


@main_bp.route('/blogs')
def blogs():
    """
    Display all published blog posts.
    
    Returns:
        Response: Blog listing page
    """
    page = request.args.get('page', 1, type=int)
    per_page = 6  # Number of posts per page
    
    posts = BlogPost.query.filter_by(is_published=True)\
                          .order_by(BlogPost.created_at.desc())\
                          .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('public/blogs/index.html', posts=posts)


@main_bp.route('/blogs/<int:id>')
def blog_detail(id):
    """
    Display a single blog post.
    
    Args:
        id: Blog post ID
        
    Returns:
        Response: Blog detail page
    """
    post = BlogPost.query.filter_by(id=id, is_published=True).first_or_404()
    return render_template('public/blogs/detail.html', post=post)


@main_bp.route('/stories')
def god_stories():
    """
    Display all published God stories.
    
    Returns:
        Response: God stories listing page
    """
    page = request.args.get('page', 1, type=int)
    per_page = 6  # Number of stories per page
    
    stories = GodStory.query.filter_by(is_published=True)\
                           .order_by(GodStory.created_at.desc())\
                           .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('public/stories/index.html', stories=stories)


@main_bp.route('/stories/<int:id>')
def story_detail(id):
    """
    Display a single God story.
    
    Args:
        id: Story ID
        
    Returns:
        Response: Story detail page
    """
    story = GodStory.query.filter_by(id=id, is_published=True).first_or_404()
    return render_template('public/stories/detail.html', story=story)


@main_bp.route('/music')
def music():
    """
    Display all published songs.
    
    Returns:
        Response: Music listing page
    """
    page = request.args.get('page', 1, type=int)
    per_page = 12  # Number of songs per page
    
    songs = Song.query.filter_by(is_published=True)\
                     .order_by(Song.created_at.desc())\
                     .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('public/music/index.html', songs=songs)


@main_bp.route('/music/<int:id>')
def music_detail(id):
    """
    Display a single song.
    
    Args:
        id: Song ID
        
    Returns:
        Response: Song detail page
    """
    song = Song.query.filter_by(id=id, is_published=True).first_or_404()
    return render_template('public/music/detail.html', song=song)


@main_bp.route('/testimonials')
def testimonials():
    """
    Display all approved testimonials.
    
    Returns:
        Response: Testimonials listing page
    """
    page = request.args.get('page', 1, type=int)
    per_page = 9  # Number of testimonials per page
    
    testimonials = Testimonial.query.filter_by(is_published=True, is_approved=True)\
                                   .order_by(Testimonial.created_at.desc())\
                                   .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('public/testimonials/index.html', testimonials=testimonials)


@main_bp.route('/testimonials/<int:id>')
def testimonial_detail(id):
    """
    Display a single testimonial.
    
    Args:
        id: Testimonial ID
        
    Returns:
        Response: Testimonial detail page
    """
    testimonial = Testimonial.query.filter_by(id=id, is_published=True, is_approved=True).first_or_404()
    return render_template('public/testimonials/detail.html', testimonial=testimonial)


@main_bp.route('/radio')
def radio():
    """
    Display all published radio sessions.
    
    Returns:
        Response: Radio sessions listing page
    """
    page = request.args.get('page', 1, type=int)
    per_page = 8  # Number of sessions per page
    
    sessions = RadioSession.query.filter_by(is_published=True)\
                                .order_by(RadioSession.created_at.desc())\
                                .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('public/radio/index.html', sessions=sessions)


@main_bp.route('/radio/<int:id>')
def radio_detail(id):
    """
    Display a single radio session.
    
    Args:
        id: Radio session ID
        
    Returns:
        Response: Radio session detail page
    """
    session = RadioSession.query.filter_by(id=id, is_published=True).first_or_404()
    return render_template('public/radio/detail.html', session=session)


# Admin Dashboard
@main_bp.route('/admin')
@login_required
def admin_dashboard():
    """
    Display admin dashboard.
    
    Returns:
        Response: Admin dashboard page
    """
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    # Get basic statistics
    stats = {
        'total_users': User.query.count(),
        'total_posts': BlogPost.query.count(),
        'total_stories': GodStory.query.count(),
        'total_songs': Song.query.count(),
        'total_testimonials': Testimonial.query.count(),
        'total_radio_sessions': RadioSession.query.count(),
    }
    
    return render_template('private/dashboard.html', stats=stats)


# Media Serving Routes
@main_bp.route('/radio/<int:session_id>/audio')
def serve_radio_session_audio(session_id):
    """Serve radio session audio file for public playback."""
    radio_session = RadioSession.query.filter_by(id=session_id, is_published=True).first_or_404()
    
    if not radio_session.file_data:
        abort(404)
    
    # Simple MIME type detection based on common audio formats
    mime_type = 'audio/mpeg'  # Default to MP3
    
    return Response(
        radio_session.file_data,
        mimetype=mime_type,
        headers={
            'Content-Disposition': f'inline; filename="{radio_session.title}.mp3"',
            'Cache-Control': 'no-cache'
        }
    )


@main_bp.route('/stories/<int:story_id>/audio')
def serve_story_audio(story_id):
    """Serve god story audio file for public playback."""
    story = GodStory.query.filter_by(id=story_id, is_published=True).first_or_404()
    
    if not story.audio_data:
        abort(404)
    
    # Simple MIME type detection based on common audio formats
    mime_type = 'audio/mpeg'  # Default to MP3
    
    return Response(
        story.audio_data,
        mimetype=mime_type,
        headers={
            'Content-Disposition': f'inline; filename="{story.title}_audio.mp3"',
            'Cache-Control': 'no-cache'
        }
    )


@main_bp.route('/stories/<int:story_id>/video')
def serve_story_video(story_id):
    """Serve god story video file for public playback."""
    story = GodStory.query.filter_by(id=story_id, is_published=True).first_or_404()
    
    if not story.video_data:
        abort(404)
    
    # Simple MIME type detection based on common video formats
    mime_type = 'video/mp4'  # Default to MP4
    
    return Response(
        story.video_data,
        mimetype=mime_type,
        headers={
            'Content-Disposition': f'inline; filename="{story.title}_video.mp4"',
            'Cache-Control': 'no-cache'
        }
    )


@main_bp.route('/songs/<int:song_id>/audio')
def serve_song_audio(song_id):
    """Serve song audio file for public playback."""
    song = Song.query.filter_by(id=song_id, is_published=True).first_or_404()
    
    if not song.file_data:
        abort(404)
    
    # Simple MIME type detection based on common audio formats
    mime_type = 'audio/mpeg'  # Default to MP3
    
    return Response(
        song.file_data,
        mimetype=mime_type,
        headers={
            'Content-Disposition': f'inline; filename="{song.title}.mp3"',
            'Cache-Control': 'no-cache'
        }
    )
