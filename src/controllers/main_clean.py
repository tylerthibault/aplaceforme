from flask import Blueprint, render_template, request, abort, flash, redirect, url_for, Response
from typing import Tuple
from datetime import datetime
from src.models import BlogPost, GodStory, Song, Testimonial, RadioSession, User
from src import db
from flask_login import login_required, current_user

# Create main blueprint
main_bp = Blueprint('main', __name__)

# File format constants
ALLOWED_AUDIO_TYPES = {
    'audio/mpeg',       # MP3
    'audio/wav',        # WAV
    'audio/ogg',        # OGG
    'audio/mp4',        # MP4 audio
    'video/mp4',        # MP4 video (can contain audio)
    'audio/x-m4a',      # M4A (alternative MIME type)
    'audio/m4a',        # M4A (standard MIME type)
    'audio/aac',        # AAC
    'audio/flac'        # FLAC
}

ALLOWED_IMAGE_TYPES = {
    'image/jpeg',
    'image/png', 
    'image/gif',
    'image/webp'
}

ALLOWED_VIDEO_TYPES = {
    'video/mp4',
    'video/webm',
    'video/quicktime',
    'video/x-msvideo'
}


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


@main_bp.route('/')
def index():
    """
    Display the home page.
    
    Returns:
        Response: Home page template
    """
    return render_template('public/landing/index.html')


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


# Admin management routes
@main_bp.route('/admin/users')
@login_required
def admin_users():
    """Display all users for admin management."""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    users = User.query.paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('admin/users.html', users=users, pagination=users, title='Manage Users', add_url=url_for('main.admin_user_new'))


@main_bp.route('/admin/blog-posts')
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
    
    return render_template('admin/blog_posts.html', posts=posts, pagination=posts, title='Manage Blog Posts', add_url=url_for('main.admin_blog_post_new'))


@main_bp.route('/admin/god-stories')
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
    
    return render_template('admin/god_stories.html', stories=stories, pagination=stories, title='Manage God Stories', add_url=url_for('main.admin_god_story_new'))


@main_bp.route('/admin/songs')
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
    
    return render_template('admin/songs.html', songs=songs, pagination=songs, title='Manage Songs', add_url=url_for('main.admin_song_new'))


@main_bp.route('/admin/testimonials')
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
    
    return render_template('admin/testimonials.html', testimonials=testimonials, pagination=testimonials, title='Manage Testimonials', add_url=url_for('main.admin_testimonial_new'))


@main_bp.route('/admin/radio-sessions')
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
    
    return render_template('admin/radio_sessions.html', sessions=sessions, pagination=sessions, title='Manage Radio Sessions', add_url=url_for('main.admin_radio_session_new'))


@main_bp.route('/admin/radio-sessions/new', methods=['GET', 'POST'])
@login_required
def admin_radio_session_new():
    """Add new radio session form and handler."""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        host = request.form.get('host', '').strip()
        guests = request.form.get('guests', '').strip()
        tags = request.form.get('tags', '').strip()
        category = request.form.get('category', '').strip()
        bible_references = request.form.get('bible_references', '').strip()
        show_notes = request.form.get('show_notes', '').strip()
        episode_number = request.form.get('episode_number', '').strip()
        season_number = request.form.get('season_number', '').strip()
        duration = request.form.get('duration', '').strip()
        status = request.form.get('status', 'draft')
        publish_at = request.form.get('publish_at', '').strip()
        featured = bool(request.form.get('featured'))
        allow_download = bool(request.form.get('allow_download'))
        allow_comments = bool(request.form.get('allow_comments'))
        
        # Handle file uploads
        audio_file = request.files.get('audio_file')
        thumbnail = request.files.get('thumbnail')
        
        # Validate inputs
        errors = []
        
        if not title:
            errors.append('Title is required')
        elif len(title) > 200:
            errors.append('Title must be less than 200 characters')
            
        if not audio_file or not audio_file.filename:
            errors.append('Audio file is required')
            
        # Validate episode number if provided
        if episode_number:
            try:
                episode_number = int(episode_number)
                if episode_number < 1:
                    errors.append('Episode number must be at least 1')
            except ValueError:
                errors.append('Episode number must be a valid number')
        else:
            episode_number = None
            
        # Validate season number if provided
        if season_number:
            try:
                season_number = int(season_number)
                if season_number < 1:
                    errors.append('Season number must be at least 1')
            except ValueError:
                errors.append('Season number must be a valid number')
        else:
            season_number = None
            
        # Validate duration if provided
        if duration:
            try:
                duration = int(duration)
                if duration < 1:
                    errors.append('Duration must be at least 1 second')
            except ValueError:
                errors.append('Duration must be a valid number')
        else:
            duration = None
            
        # Validate publish date for scheduled status
        parsed_publish_at = None
        if status == 'scheduled':
            if not publish_at:
                errors.append('Publish date is required for scheduled episodes')
            else:
                try:
                    parsed_publish_at = datetime.strptime(publish_at, '%Y-%m-%dT%H:%M')
                    if parsed_publish_at <= datetime.now():
                        errors.append('Publish date must be in the future')
                except ValueError:
                    errors.append('Invalid publish date format')
            
        # Validate file uploads
        if audio_file and audio_file.filename:
            if audio_file.content_type not in ALLOWED_AUDIO_TYPES:
                errors.append('Invalid audio format. Please use MP3, WAV, OGG, MP4, M4A, AAC, or FLAC.')
            elif len(audio_file.read()) > 100 * 1024 * 1024:  # 100MB limit
                errors.append('Audio file too large. Maximum size is 100MB.')
            audio_file.seek(0)  # Reset file pointer
            
        if thumbnail and thumbnail.filename:
            if thumbnail.content_type not in ALLOWED_IMAGE_TYPES:
                errors.append('Invalid image format. Please use JPEG, PNG, GIF, or WebP.')
            elif len(thumbnail.read()) > 5 * 1024 * 1024:  # 5MB limit
                errors.append('Image file too large. Maximum size is 5MB.')
            thumbnail.seek(0)  # Reset file pointer
            
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('admin/forms/radio_session_form.html', 
                                 title='Add New Radio Session',
                                 form_title='Add New Radio Session',
                                 form_description='Create a new radio episode.',
                                 cancel_url=url_for('main.admin_radio_sessions'))
        
        # Create new radio session
        try:
            radio_session = RadioSession(
                title=title,
                description=description if description else None,
                host=host if host else None,
                guests=guests if guests else None,
                category=category if category else None,
                bible_references=bible_references if bible_references else None,
                show_notes=show_notes if show_notes else None,
                episode_number=episode_number,
                season_number=season_number,
                duration=duration,
                status=status,
                featured=featured,
                allow_download=allow_download,
                allow_comments=allow_comments,
                uploaded_by=current_user.id
            )
            
            # Set tags
            if tags:
                radio_session.set_tags([tag.strip() for tag in tags.split(',') if tag.strip()])
            
            # Handle file data
            if audio_file and audio_file.filename:
                radio_session.file_data = audio_file.read()
                
            if thumbnail and thumbnail.filename:
                radio_session.thumbnail_data = thumbnail.read()
            
            # Handle publishing
            if status == 'published':
                radio_session.publish()
            elif status == 'scheduled' and parsed_publish_at:
                radio_session.schedule_publish(parsed_publish_at)
            
            db.session.add(radio_session)
            db.session.commit()
            
            flash('Radio session created successfully!', 'success')
            return redirect(url_for('main.admin_radio_sessions'))
            
        except Exception as e:
            db.session.rollback()
            flash('Failed to create radio session. Please try again.', 'error')
            return render_template('admin/forms/radio_session_form.html', 
                                 title='Add New Radio Session',
                                 form_title='Add New Radio Session',
                                 form_description='Create a new radio episode.',
                                 cancel_url=url_for('main.admin_radio_sessions'))
    
    return render_template('admin/forms/radio_session_form.html', 
                         title='Add New Radio Session',
                         form_title='Add New Radio Session',
                         form_description='Create a new radio episode.',
                         cancel_url=url_for('main.admin_radio_sessions'))


@main_bp.route('/admin/radio-sessions/<int:session_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_radio_session_edit(session_id):
    """Edit radio session form and handler."""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    radio_session = RadioSession.query.get_or_404(session_id)
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        host = request.form.get('host', '').strip()
        guests = request.form.get('guests', '').strip()
        tags = request.form.get('tags', '').strip()
        category = request.form.get('category', '').strip()
        bible_references = request.form.get('bible_references', '').strip()
        show_notes = request.form.get('show_notes', '').strip()
        episode_number = request.form.get('episode_number', '').strip()
        season_number = request.form.get('season_number', '').strip()
        duration = request.form.get('duration', '').strip()
        status = request.form.get('status', 'draft')
        publish_at = request.form.get('publish_at', '').strip()
        featured = bool(request.form.get('featured'))
        allow_download = bool(request.form.get('allow_download'))
        allow_comments = bool(request.form.get('allow_comments'))
        
        # Handle file uploads
        audio_file = request.files.get('audio_file')
        thumbnail = request.files.get('thumbnail')
        
        # Validate inputs
        errors = []
        
        if not title:
            errors.append('Title is required')
        elif len(title) > 200:
            errors.append('Title must be less than 200 characters')
            
        # Validate episode number if provided
        if episode_number:
            try:
                episode_number = int(episode_number)
                if episode_number < 1:
                    errors.append('Episode number must be at least 1')
            except ValueError:
                errors.append('Episode number must be a valid number')
        else:
            episode_number = None
            
        # Validate season number if provided
        if season_number:
            try:
                season_number = int(season_number)
                if season_number < 1:
                    errors.append('Season number must be at least 1')
            except ValueError:
                errors.append('Season number must be a valid number')
        else:
            season_number = None
            
        # Validate duration if provided
        if duration:
            try:
                duration = int(duration)
                if duration < 1:
                    errors.append('Duration must be at least 1 second')
            except ValueError:
                errors.append('Duration must be a valid number')
        else:
            duration = None
            
        # Validate publish date for scheduled status
        parsed_publish_at = None
        if status == 'scheduled':
            if not publish_at:
                errors.append('Publish date is required for scheduled episodes')
            else:
                try:
                    parsed_publish_at = datetime.strptime(publish_at, '%Y-%m-%dT%H:%M')
                    if parsed_publish_at <= datetime.now():
                        errors.append('Publish date must be in the future')
                except ValueError:
                    errors.append('Invalid publish date format')
            
        # Validate file uploads
        if audio_file and audio_file.filename:
            if audio_file.content_type not in ALLOWED_AUDIO_TYPES:
                errors.append('Invalid audio format. Please use MP3, WAV, OGG, MP4, M4A, AAC, or FLAC.')
            elif len(audio_file.read()) > 100 * 1024 * 1024:  # 100MB limit
                errors.append('Audio file too large. Maximum size is 100MB.')
            audio_file.seek(0)  # Reset file pointer
            
        if thumbnail and thumbnail.filename:
            if thumbnail.content_type not in ALLOWED_IMAGE_TYPES:
                errors.append('Invalid image format. Please use JPEG, PNG, GIF, or WebP.')
            elif len(thumbnail.read()) > 5 * 1024 * 1024:  # 5MB limit
                errors.append('Image file too large. Maximum size is 5MB.')
            thumbnail.seek(0)  # Reset file pointer
            
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('admin/forms/radio_session_form.html', 
                                 radio_session=radio_session,
                                 title='Edit Radio Session',
                                 form_title='Edit Radio Session',
                                 form_description='Edit this radio session.',
                                 cancel_url=url_for('main.admin_radio_sessions'))
        
        # Update radio session
        try:
            radio_session.title = title
            radio_session.description = description if description else None
            radio_session.host = host if host else None
            radio_session.guests = guests if guests else None
            radio_session.category = category if category else None
            radio_session.bible_references = bible_references if bible_references else None
            radio_session.show_notes = show_notes if show_notes else None
            radio_session.episode_number = episode_number
            radio_session.season_number = season_number
            radio_session.duration = duration
            radio_session.status = status
            radio_session.featured = featured
            radio_session.allow_download = allow_download
            radio_session.allow_comments = allow_comments
            
            # Set tags
            if tags:
                radio_session.set_tags([tag.strip() for tag in tags.split(',') if tag.strip()])
            else:
                radio_session.tags = None
            
            # Handle file data updates
            if audio_file and audio_file.filename:
                radio_session.file_data = audio_file.read()
                
            if thumbnail and thumbnail.filename:
                radio_session.thumbnail_data = thumbnail.read()
            
            # Handle publishing status changes
            if status == 'published' and not radio_session.is_published:
                radio_session.publish()
            elif status == 'scheduled' and parsed_publish_at:
                radio_session.schedule_publish(parsed_publish_at)
            elif status == 'draft' and radio_session.is_published:
                radio_session.unpublish()
            
            db.session.commit()
            
            flash('Radio session updated successfully!', 'success')
            return redirect(url_for('main.admin_radio_sessions'))
            
        except Exception as e:
            db.session.rollback()
            flash('Failed to update radio session. Please try again.', 'error')
            return render_template('admin/forms/radio_session_form.html', 
                                 radio_session=radio_session,
                                 title='Edit Radio Session',
                                 form_title='Edit Radio Session',
                                 form_description='Edit this radio session.',
                                 cancel_url=url_for('main.admin_radio_sessions'))
    
    return render_template('admin/forms/radio_session_form.html', 
                         radio_session=radio_session,
                         title='Edit Radio Session',
                         form_title='Edit Radio Session',
                         form_description='Edit this radio session.',
                         cancel_url=url_for('main.admin_radio_sessions'))


@main_bp.route('/admin/radio-sessions/<int:session_id>/delete', methods=['POST'])
@login_required
def admin_radio_session_delete(session_id):
    """Delete radio session."""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    radio_session = RadioSession.query.get_or_404(session_id)
    
    try:
        db.session.delete(radio_session)
        db.session.commit()
        flash('Radio session deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Failed to delete radio session. Please try again.', 'error')
    
    return redirect(url_for('main.admin_radio_sessions'))


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


# TODO: Add other admin routes for creating/editing blog posts, god stories, songs, testimonials, and users
