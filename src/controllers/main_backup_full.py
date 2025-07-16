from flask import Blueprint, render_template, request, abort, flash, redirect, url_for, Response
from typing import Tuple
from datetime import datetime
import logging
from src.models import BlogPost, GodStory, Song, Testimonial, RadioSession, User
from src import db
from flask_login import login_required, current_user

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

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
        logger.info("Processing POST request for new radio session")
        
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
        
        logger.debug(f"Form data received - title: '{title}', status: '{status}', episode_number: '{episode_number}'")
        
        # Handle file uploads
        audio_file = request.files.get('audio_file')
        thumbnail = request.files.get('thumbnail')
        
        logger.debug(f"Files received - audio_file: {audio_file.filename if audio_file else None}, thumbnail: {thumbnail.filename if thumbnail else None}")
        
        # Validate inputs
        errors = []
        logger.info("Starting form validation")
        
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
            logger.warning(f"Validation errors found: {errors}")
            for error in errors:
                flash(error, 'error')
            return render_template('admin/forms/radio_session_form.html', 
                                 title='Add New Radio Session',
                                 form_title='Add New Radio Session',
                                 form_description='Create a new radio episode.',
                                 cancel_url=url_for('main.admin_radio_sessions'))
        
        logger.info("Form validation passed successfully")
        
        # Create new radio session
        try:
            logger.info(f"Starting radio session creation for user {current_user.id}")
            logger.debug(f"Radio session data: title='{title}', host='{host}', status='{status}', featured={featured}")
            
            radio_session = RadioSession(
                title=title,
                description=description if description else None,
                episode_number=episode_number,
                season_number=season_number,
                duration=duration,
                status=status,
                uploaded_by=current_user.id
            )
            logger.info("RadioSession object created successfully")
            
            # Log fields that are not stored in the model yet
            if host or guests or category or bible_references or show_notes:
                logger.warning(f"Additional fields ignored (not in model): host='{host}', guests='{guests}', category='{category}', bible_references='{bible_references}', show_notes='{show_notes}'")
            if featured or allow_download or allow_comments:
                logger.warning(f"Boolean flags ignored (not in model): featured={featured}, allow_download={allow_download}, allow_comments={allow_comments}")
            
            # Set tags
            if tags:
                logger.debug(f"Setting tags: {tags}")
                radio_session.set_tags([tag.strip() for tag in tags.split(',') if tag.strip()])
                logger.info(f"Tags set successfully: {radio_session.get_tags_list()}")
            
            # Handle file data
            if audio_file and audio_file.filename:
                logger.info(f"Processing audio file: {audio_file.filename}, content_type: {audio_file.content_type}")
                audio_data = audio_file.read()
                logger.debug(f"Audio file size: {len(audio_data)} bytes")
                radio_session.file_data = audio_data
                logger.info("Audio file data set successfully")
                
            if thumbnail and thumbnail.filename:
                logger.info(f"Processing thumbnail: {thumbnail.filename}, content_type: {thumbnail.content_type}")
                thumbnail_data = thumbnail.read()
                logger.debug(f"Thumbnail file size: {len(thumbnail_data)} bytes")
                radio_session.thumbnail_data = thumbnail_data
                logger.info("Thumbnail data set successfully")
            
            # Handle publishing
            if status == 'published':
                logger.info("Publishing radio session immediately")
                radio_session.publish()
                logger.info("Radio session published successfully")
            elif status == 'scheduled' and parsed_publish_at:
                logger.info(f"Scheduling radio session for: {parsed_publish_at}")
                radio_session.schedule_publish(parsed_publish_at)
                logger.info("Radio session scheduled successfully")
            
            logger.info("Adding radio session to database session")
            db.session.add(radio_session)
            
            logger.info("Committing changes to database")
            db.session.commit()
            logger.info(f"Radio session created successfully with ID: {radio_session.id}")
            logger.info(f"Saved fields - title: '{radio_session.title}', episode: {radio_session.episode_number}, duration: {radio_session.duration}")
            
            flash('Radio session created successfully!', 'success')
            return redirect(url_for('main.admin_radio_sessions'))
            
        except Exception as e:
            logger.error(f"Error creating radio session: {str(e)}", exc_info=True)
            db.session.rollback()
            logger.info("Database session rolled back")
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
            radio_session.episode_number = episode_number
            radio_session.season_number = season_number
            radio_session.duration = duration
            radio_session.status = status
            
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


@main_bp.route('/songs/<int:song_id>/audio')
def serve_song_audio(song_id):
    """Serve song audio file for public playback."""
    song = Song.query.filter_by(id=song_id, is_published=True).first_or_404()
    
    if not song.audio_data:
        abort(404)
    
    # Simple MIME type detection based on common audio formats
    mime_type = 'audio/mpeg'  # Default to MP3
    
    return Response(
        song.audio_data,
        mimetype=mime_type,
        headers={
            'Content-Disposition': f'inline; filename="{song.title}.mp3"',
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


# TODO: Add other admin routes for creating/editing blog posts, god stories, songs, testimonials, and users

@main_bp.route('/admin/users/new', methods=['GET', 'POST'])
@login_required
def admin_user_new():
    """Add new user form and handler."""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        # TODO: Implement user creation logic
        flash('User creation not yet implemented.', 'warning')
        return redirect(url_for('main.admin_users'))
    
    # TODO: Create user form template
    flash('User creation form not yet implemented.', 'warning')
    return redirect(url_for('main.admin_users'))


@main_bp.route('/admin/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_user_edit(user_id):
    """Edit user form and handler."""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        # TODO: Implement user edit logic
        flash('User editing not yet implemented.', 'warning')
        return redirect(url_for('main.admin_users'))
    
    # TODO: Create user edit form template
    flash('User editing form not yet implemented.', 'warning')
    return redirect(url_for('main.admin_users'))


@main_bp.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@login_required
def admin_user_delete(user_id):
    """Delete user."""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    user = User.query.get_or_404(user_id)
    
    # TODO: Implement user deletion logic
    flash('User deletion not yet implemented.', 'warning')
    return redirect(url_for('main.admin_users'))


@main_bp.route('/admin/blog-posts/new', methods=['GET', 'POST'])
@login_required
def admin_blog_post_new():
    """Add new blog post form and handler."""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        logger.info("Processing POST request for new blog post")
        
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        author_name = request.form.get('author_name', '').strip()
        category = request.form.get('category', '').strip()
        tags = request.form.get('tags', '').strip()
        status = request.form.get('status', 'draft')
        publish_at = request.form.get('publish_at', '').strip()
        featured = bool(request.form.get('featured'))
        allow_comments = bool(request.form.get('allow_comments'))
        
        # Handle file upload
        featured_image = request.files.get('featured_image')
        
        logger.debug(f"Form data received - title: '{title}', status: '{status}', featured: {featured}")
        
        # Validate inputs
        errors = []
        logger.info("Starting form validation")
        
        if not title:
            errors.append('Title is required')
        elif len(title) > 200:
            errors.append('Title must be less than 200 characters')
            
        if not content:
            errors.append('Content is required')
            
        # Validate publish date for scheduled status
        parsed_publish_at = None
        if status == 'scheduled':
            if not publish_at:
                errors.append('Publish date is required for scheduled posts')
            else:
                try:
                    parsed_publish_at = datetime.strptime(publish_at, '%Y-%m-%dT%H:%M')
                    if parsed_publish_at <= datetime.now():
                        errors.append('Publish date must be in the future')
                except ValueError:
                    errors.append('Invalid publish date format')
        
        # Validate image upload
        if featured_image and featured_image.filename:
            if featured_image.content_type not in ALLOWED_IMAGE_TYPES:
                errors.append('Invalid image format. Please use JPEG, PNG, GIF, or WebP.')
            elif len(featured_image.read()) > 5 * 1024 * 1024:  # 5MB limit
                errors.append('Image file too large. Maximum size is 5MB.')
            featured_image.seek(0)  # Reset file pointer
            
        if errors:
            logger.warning(f"Validation errors found: {errors}")
            for error in errors:
                flash(error, 'error')
            return render_template('admin/forms/blog_post_form.html', 
                                 title='Add New Blog Post',
                                 form_title='Add New Blog Post',
                                 form_description='Create a new blog post.',
                                 cancel_url=url_for('main.admin_blog_posts'))
        
        logger.info("Form validation passed successfully")
        
        # Create new blog post
        try:
            logger.info(f"Starting blog post creation for user {current_user.id}")
            logger.debug(f"Blog post data: title='{title}', status='{status}', featured={featured}")
            
            blog_post = BlogPost(
                title=title,
                content=content,
                author_id=current_user.id,
                status=status
            )
            logger.info("BlogPost object created successfully")
            
            # Log fields that are not stored in the model yet
            if author_name or category or tags or featured or allow_comments:
                logger.warning(f"Additional fields ignored (not in model): author_name='{author_name}', category='{category}', tags='{tags}', featured={featured}, allow_comments={allow_comments}")
            
            # Handle image data
            if featured_image and featured_image.filename:
                logger.info(f"Processing featured image: {featured_image.filename}, content_type: {featured_image.content_type}")
                image_data = featured_image.read()
                logger.debug(f"Image file size: {len(image_data)} bytes")
                blog_post.image_data = image_data
                logger.info("Featured image data set successfully")
            
            # Handle publishing
            if status == 'published':
                logger.info("Publishing blog post immediately")
                blog_post.publish()
                logger.info("Blog post published successfully")
            elif status == 'scheduled' and parsed_publish_at:
                logger.info(f"Scheduling blog post for: {parsed_publish_at}")
                blog_post.schedule_publish(parsed_publish_at)
                logger.info("Blog post scheduled successfully")
            
            logger.info("Adding blog post to database session")
            db.session.add(blog_post)
            
            logger.info("Committing changes to database")
            db.session.commit()
            logger.info(f"Blog post created successfully with ID: {blog_post.id}")
            logger.info(f"Saved fields - title: '{blog_post.title}', status: '{blog_post.status}', author_id: {blog_post.author_id}")
            
            flash('Blog post created successfully!', 'success')
            return redirect(url_for('main.admin_blog_posts'))
            
        except Exception as e:
            logger.error(f"Error creating blog post: {str(e)}", exc_info=True)
            db.session.rollback()
            logger.info("Database session rolled back")
            flash('Failed to create blog post. Please try again.', 'error')
            return render_template('admin/forms/blog_post_form.html', 
                                 title='Add New Blog Post',
                                 form_title='Add New Blog Post',
                                 form_description='Create a new blog post.',
                                 cancel_url=url_for('main.admin_blog_posts'))
    
    return render_template('admin/forms/blog_post_form.html', 
                         title='Add New Blog Post',
                         form_title='Add New Blog Post',
                         form_description='Create a new blog post.',
                         cancel_url=url_for('main.admin_blog_posts'))


@main_bp.route('/admin/blog-posts/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_blog_post_edit(post_id):
    """Edit blog post form and handler."""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    blog_post = BlogPost.query.get_or_404(post_id)
    
    if request.method == 'POST':
        logger.info(f"Processing POST request to edit blog post {post_id}")
        
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        author_name = request.form.get('author_name', '').strip()
        category = request.form.get('category', '').strip()
        tags = request.form.get('tags', '').strip()
        status = request.form.get('status', 'draft')
        publish_at = request.form.get('publish_at', '').strip()
        featured = bool(request.form.get('featured'))
        allow_comments = bool(request.form.get('allow_comments'))
        
        # Handle file upload
        featured_image = request.files.get('featured_image')
        
        logger.debug(f"Form data received - title: '{title}', status: '{status}', featured: {featured}")
        
        # Validate inputs
        errors = []
        
        if not title:
            errors.append('Title is required')
        elif len(title) > 200:
            errors.append('Title must be less than 200 characters')
            
        if not content:
            errors.append('Content is required')
            
        # Validate publish date for scheduled status
        parsed_publish_at = None
        if status == 'scheduled':
            if not publish_at:
                errors.append('Publish date is required for scheduled posts')
            else:
                try:
                    parsed_publish_at = datetime.strptime(publish_at, '%Y-%m-%dT%H:%M')
                    if parsed_publish_at <= datetime.now():
                        errors.append('Publish date must be in the future')
                except ValueError:
                    errors.append('Invalid publish date format')
        
        # Validate image upload
        if featured_image and featured_image.filename:
            if featured_image.content_type not in ALLOWED_IMAGE_TYPES:
                errors.append('Invalid image format. Please use JPEG, PNG, GIF, or WebP.')
            elif len(featured_image.read()) > 5 * 1024 * 1024:  # 5MB limit
                errors.append('Image file too large. Maximum size is 5MB.')
            featured_image.seek(0)  # Reset file pointer
            
        if errors:
            logger.warning(f"Validation errors found: {errors}")
            for error in errors:
                flash(error, 'error')
            return render_template('admin/forms/blog_post_form.html', 
                                 blog_post=blog_post,
                                 title='Edit Blog Post',
                                 form_title='Edit Blog Post',
                                 form_description='Edit this blog post.',
                                 cancel_url=url_for('main.admin_blog_posts'))
        
        # Update blog post
        try:
            logger.info(f"Updating blog post {post_id}")
            
            blog_post.title = title
            blog_post.content = content
            blog_post.status = status
            
            # Handle image data updates
            if featured_image and featured_image.filename:
                logger.info(f"Processing new featured image: {featured_image.filename}")
                image_data = featured_image.read()
                blog_post.image_data = image_data
                logger.info("Featured image updated successfully")
            
            # Handle publishing status changes
            if status == 'published' and not blog_post.is_published:
                logger.info("Publishing blog post")
                blog_post.publish()
            elif status == 'scheduled' and parsed_publish_at:
                logger.info(f"Scheduling blog post for: {parsed_publish_at}")
                blog_post.schedule_publish(parsed_publish_at)
            elif status == 'draft' and blog_post.is_published:
                logger.info("Unpublishing blog post")
                blog_post.unpublish()
            
            db.session.commit()
            logger.info(f"Blog post {post_id} updated successfully")
            
            flash('Blog post updated successfully!', 'success')
            return redirect(url_for('main.admin_blog_posts'))
            
        except Exception as e:
            logger.error(f"Error updating blog post {post_id}: {str(e)}", exc_info=True)
            db.session.rollback()
            flash('Failed to update blog post. Please try again.', 'error')
            return render_template('admin/forms/blog_post_form.html', 
                                 blog_post=blog_post,
                                 title='Edit Blog Post',
                                 form_title='Edit Blog Post',
                                 form_description='Edit this blog post.',
                                 cancel_url=url_for('main.admin_blog_posts'))
    
    return render_template('admin/forms/blog_post_form.html', 
                         blog_post=blog_post,
                         title='Edit Blog Post',
                         form_title='Edit Blog Post',
                         form_description='Edit this blog post.',
                         cancel_url=url_for('main.admin_blog_posts'))


@main_bp.route('/admin/blog-posts/<int:post_id>/delete', methods=['POST'])
@login_required
def admin_blog_post_delete(post_id):
    """Delete blog post."""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    blog_post = BlogPost.query.get_or_404(post_id)
    
    try:
        logger.info(f"Deleting blog post {post_id}: '{blog_post.title}'")
        db.session.delete(blog_post)
        db.session.commit()
        logger.info(f"Blog post {post_id} deleted successfully")
        flash('Blog post deleted successfully!', 'success')
    except Exception as e:
        logger.error(f"Error deleting blog post {post_id}: {str(e)}", exc_info=True)
        db.session.rollback()
        flash('Failed to delete blog post. Please try again.', 'error')
    
    return redirect(url_for('main.admin_blog_posts'))


@main_bp.route('/admin/god-stories/new', methods=['GET', 'POST'])
@login_required
def admin_god_story_new():
    """Add new God story form and handler."""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        # TODO: Implement God story creation logic
        flash('God story creation not yet implemented.', 'warning')
        return redirect(url_for('main.admin_god_stories'))
    
    # TODO: Create God story form template
    flash('God story creation form not yet implemented.', 'warning')
    return redirect(url_for('main.admin_god_stories'))


@main_bp.route('/admin/god-stories/<int:story_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_god_story_edit(story_id):
    """Edit God story form and handler."""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    story = GodStory.query.get_or_404(story_id)
    
    if request.method == 'POST':
        # TODO: Implement God story edit logic
        flash('God story editing not yet implemented.', 'warning')
        return redirect(url_for('main.admin_god_stories'))
    
    # TODO: Create God story edit form template
    flash('God story editing form not yet implemented.', 'warning')
    return redirect(url_for('main.admin_god_stories'))


@main_bp.route('/admin/god-stories/<int:story_id>/delete', methods=['POST'])
@login_required
def admin_god_story_delete(story_id):
    """Delete God story."""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    story = GodStory.query.get_or_404(story_id)
    
    # TODO: Implement God story deletion logic
    flash('God story deletion not yet implemented.', 'warning')
    return redirect(url_for('main.admin_god_stories'))


@main_bp.route('/admin/songs/new', methods=['GET', 'POST'])
@login_required
def admin_song_new():
    """Add new song form and handler."""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        # TODO: Implement song creation logic
        flash('Song creation not yet implemented.', 'warning')
        return redirect(url_for('main.admin_songs'))
    
    # TODO: Create song form template
    flash('Song creation form not yet implemented.', 'warning')
    return redirect(url_for('main.admin_songs'))


@main_bp.route('/admin/songs/<int:song_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_song_edit(song_id):
    """Edit song form and handler."""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    song = Song.query.get_or_404(song_id)
    
    if request.method == 'POST':
        # TODO: Implement song edit logic
        flash('Song editing not yet implemented.', 'warning')
        return redirect(url_for('main.admin_songs'))
    
    # TODO: Create song edit form template
    flash('Song editing form not yet implemented.', 'warning')
    return redirect(url_for('main.admin_songs'))


@main_bp.route('/admin/songs/<int:song_id>/delete', methods=['POST'])
@login_required
def admin_song_delete(song_id):
    """Delete song."""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    song = Song.query.get_or_404(song_id)
    
    # TODO: Implement song deletion logic
    flash('Song deletion not yet implemented.', 'warning')
    return redirect(url_for('main.admin_songs'))


@main_bp.route('/admin/testimonials/new', methods=['GET', 'POST'])
@login_required
def admin_testimonial_new():
    """Add new testimonial form and handler."""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        logger.info("Processing POST request for new testimonial")
        
        content = request.form.get('content', '').strip()
        author_name = request.form.get('author_name', '').strip()
        author_location = request.form.get('author_location', '').strip()
        category = request.form.get('category', '').strip()
        tags = request.form.get('tags', '').strip()
        bible_verse = request.form.get('bible_verse', '').strip()
        date_of_event = request.form.get('date_of_event', '').strip()
        approval_status = request.form.get('approval_status', 'pending')
        status = request.form.get('status', 'draft')
        publish_at = request.form.get('publish_at', '').strip()
        featured = bool(request.form.get('featured'))
        allow_comments = bool(request.form.get('allow_comments'))
        
        # Handle file upload
        author_image = request.files.get('author_image')
        
        logger.debug(f"Form data received - content length: {len(content)}, approval_status: '{approval_status}', status: '{status}'")
        
        # Validate inputs
        errors = []
        logger.info("Starting form validation")
        
        if not content:
            errors.append('Testimonial content is required')
            
        # Validate publish date for scheduled status
        parsed_publish_at = None
        if status == 'scheduled':
            if not publish_at:
                errors.append('Publish date is required for scheduled testimonials')
            else:
                try:
                    parsed_publish_at = datetime.strptime(publish_at, '%Y-%m-%dT%H:%M')
                    if parsed_publish_at <= datetime.now():
                        errors.append('Publish date must be in the future')
                except ValueError:
                    errors.append('Invalid publish date format')
        
        # Validate event date
        parsed_date_of_event = None
        if date_of_event:
            try:
                parsed_date_of_event = datetime.strptime(date_of_event, '%Y-%m-%d')
            except ValueError:
                errors.append('Invalid event date format')
        
        # Validate image upload
        if author_image and author_image.filename:
            if author_image.content_type not in ALLOWED_IMAGE_TYPES:
                errors.append('Invalid image format. Please use JPEG, PNG, GIF, or WebP.')
            elif len(author_image.read()) > 5 * 1024 * 1024:  # 5MB limit
                errors.append('Image file too large. Maximum size is 5MB.')
            author_image.seek(0)  # Reset file pointer
            
        if errors:
            logger.warning(f"Validation errors found: {errors}")
            for error in errors:
                flash(error, 'error')
            return render_template('admin/forms/testimonial_form.html', 
                                 title='Add New Testimonial',
                                 form_title='Add New Testimonial',
                                 form_description='Create a new testimonial.',
                                 cancel_url=url_for('main.admin_testimonials'))
        
        logger.info("Form validation passed successfully")
        
        # Create new testimonial
        try:
            logger.info(f"Starting testimonial creation for user {current_user.id}")
            logger.debug(f"Testimonial data: content_length={len(content)}, approval_status='{approval_status}', status='{status}'")
            
            testimonial = Testimonial(
                content=content,
                author_id=current_user.id,
                status=status
            )
            logger.info("Testimonial object created successfully")
            
            # Log fields that are not stored in the model yet
            if author_name or author_location or category or tags or bible_verse or featured or allow_comments:
                logger.warning(f"Additional fields ignored (not in model): author_name='{author_name}', author_location='{author_location}', category='{category}', tags='{tags}', bible_verse='{bible_verse}', featured={featured}, allow_comments={allow_comments}")
            
            # Handle approval
            if approval_status == 'approved':
                logger.info("Approving testimonial")
                testimonial.approve(current_user.id)
                logger.info("Testimonial approved successfully")
            
            # Handle image data (store path placeholder for now since model uses image_path)
            if author_image and author_image.filename:
                logger.info(f"Processing author image: {author_image.filename}, content_type: {author_image.content_type}")
                # For now, just log that we received an image since model uses image_path, not BLOB storage
                logger.warning(f"Image upload received but not stored (model uses image_path): {author_image.filename}")
            
            # Handle publishing (only if approved)
            if status == 'published' and testimonial.is_approved:
                logger.info("Publishing testimonial immediately")
                testimonial.publish()
                logger.info("Testimonial published successfully")
            elif status == 'scheduled' and parsed_publish_at and testimonial.is_approved:
                logger.info(f"Scheduling testimonial for: {parsed_publish_at}")
                testimonial.schedule_publish(parsed_publish_at)
                logger.info("Testimonial scheduled successfully")
            elif status in ['published', 'scheduled'] and not testimonial.is_approved:
                logger.warning("Cannot publish/schedule unapproved testimonial, keeping as draft")
                testimonial.status = 'draft'
            
            logger.info("Adding testimonial to database session")
            db.session.add(testimonial)
            
            logger.info("Committing changes to database")
            db.session.commit()
            logger.info(f"Testimonial created successfully with ID: {testimonial.id}")
            logger.info(f"Saved fields - content_length: {len(testimonial.content)}, status: '{testimonial.status}', approved: {testimonial.is_approved}")
            
            flash('Testimonial created successfully!', 'success')
            return redirect(url_for('main.admin_testimonials'))
            
        except ValueError as ve:
            logger.error(f"Validation error creating testimonial: {str(ve)}")
            db.session.rollback()
            flash(str(ve), 'error')
            return render_template('admin/forms/testimonial_form.html', 
                                 title='Add New Testimonial',
                                 form_title='Add New Testimonial',
                                 form_description='Create a new testimonial.',
                                 cancel_url=url_for('main.admin_testimonials'))
        except Exception as e:
            logger.error(f"Error creating testimonial: {str(e)}", exc_info=True)
            db.session.rollback()
            logger.info("Database session rolled back")
            flash('Failed to create testimonial. Please try again.', 'error')
            return render_template('admin/forms/testimonial_form.html', 
                                 title='Add New Testimonial',
                                 form_title='Add New Testimonial',
                                 form_description='Create a new testimonial.',
                                 cancel_url=url_for('main.admin_testimonials'))
    
    return render_template('admin/forms/testimonial_form.html', 
                         title='Add New Testimonial',
                         form_title='Add New Testimonial',
                         form_description='Create a new testimonial.',
                         cancel_url=url_for('main.admin_testimonials'))


@main_bp.route('/admin/testimonials/<int:testimonial_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_testimonial_edit(testimonial_id):
    """Edit testimonial form and handler."""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    testimonial = Testimonial.query.get_or_404(testimonial_id)
    
    if request.method == 'POST':
        logger.info(f"Processing POST request to edit testimonial {testimonial_id}")
        
        content = request.form.get('content', '').strip()
        author_name = request.form.get('author_name', '').strip()
        author_location = request.form.get('author_location', '').strip()
        category = request.form.get('category', '').strip()
        tags = request.form.get('tags', '').strip()
        bible_verse = request.form.get('bible_verse', '').strip()
        date_of_event = request.form.get('date_of_event', '').strip()
        approval_status = request.form.get('approval_status', 'pending')
        status = request.form.get('status', 'draft')
        publish_at = request.form.get('publish_at', '').strip()
        featured = bool(request.form.get('featured'))
        allow_comments = bool(request.form.get('allow_comments'))
        
        # Handle file upload
        author_image = request.files.get('author_image')
        
        logger.debug(f"Form data received - content length: {len(content)}, approval_status: '{approval_status}', status: '{status}'")
        
        # Validate inputs
        errors = []
        
        if not content:
            errors.append('Testimonial content is required')
            
        # Validate publish date for scheduled status
        parsed_publish_at = None
        if status == 'scheduled':
            if not publish_at:
                errors.append('Publish date is required for scheduled testimonials')
            else:
                try:
                    parsed_publish_at = datetime.strptime(publish_at, '%Y-%m-%dT%H:%M')
                    if parsed_publish_at <= datetime.now():
                        errors.append('Publish date must be in the future')
                except ValueError:
                    errors.append('Invalid publish date format')
        
        # Validate event date
        parsed_date_of_event = None
        if date_of_event:
            try:
                parsed_date_of_event = datetime.strptime(date_of_event, '%Y-%m-%d')
            except ValueError:
                errors.append('Invalid event date format')
        
        # Validate image upload
        if author_image and author_image.filename:
            if author_image.content_type not in ALLOWED_IMAGE_TYPES:
                errors.append('Invalid image format. Please use JPEG, PNG, GIF, or WebP.')
            elif len(author_image.read()) > 5 * 1024 * 1024:  # 5MB limit
                errors.append('Image file too large. Maximum size is 5MB.')
            author_image.seek(0)  # Reset file pointer
            
        if errors:
            logger.warning(f"Validation errors found: {errors}")
            for error in errors:
                flash(error, 'error')
            return render_template('admin/forms/testimonial_form.html', 
                                 testimonial=testimonial,
                                 title='Edit Testimonial',
                                 form_title='Edit Testimonial',
                                 form_description='Edit this testimonial.',
                                 cancel_url=url_for('main.admin_testimonials'))
        
        # Update testimonial
        try:
            logger.info(f"Updating testimonial {testimonial_id}")
            
            # Store previous approval status for comparison
            was_approved = testimonial.is_approved
            
            testimonial.content = content
            testimonial.status = status
            
            # Handle approval status changes
            if approval_status == 'approved' and not was_approved:
                logger.info("Approving testimonial")
                testimonial.approve(current_user.id)
            elif approval_status == 'pending' and was_approved:
                logger.info("Removing approval from testimonial")
                testimonial.unapprove()
            
            # Handle image data updates
            if author_image and author_image.filename:
                logger.info(f"Processing new author image: {author_image.filename}")
                # For now, just log that we received an image since model uses image_path
                logger.warning(f"Image upload received but not stored (model uses image_path): {author_image.filename}")
            
            # Handle publishing status changes (only if approved)
            if status == 'published' and testimonial.is_approved and not testimonial.is_published:
                logger.info("Publishing testimonial")
                testimonial.publish()
            elif status == 'scheduled' and parsed_publish_at and testimonial.is_approved:
                logger.info(f"Scheduling testimonial for: {parsed_publish_at}")
                testimonial.schedule_publish(parsed_publish_at)
            elif status == 'draft' and testimonial.is_published:
                logger.info("Unpublishing testimonial")
                testimonial.unpublish()
            elif status in ['published', 'scheduled'] and not testimonial.is_approved:
                logger.warning("Cannot publish/schedule unapproved testimonial, keeping as draft")
                testimonial.status = 'draft'
                testimonial.is_published = False
            
            db.session.commit()
            logger.info(f"Testimonial {testimonial_id} updated successfully")
            
            flash('Testimonial updated successfully!', 'success')
            return redirect(url_for('main.admin_testimonials'))
            
        except ValueError as ve:
            logger.error(f"Validation error updating testimonial {testimonial_id}: {str(ve)}")
            db.session.rollback()
            flash(str(ve), 'error')
            return render_template('admin/forms/testimonial_form.html', 
                                 testimonial=testimonial,
                                 title='Edit Testimonial',
                                 form_title='Edit Testimonial',
                                 form_description='Edit this testimonial.',
                                 cancel_url=url_for('main.admin_testimonials'))
        except Exception as e:
            logger.error(f"Error updating testimonial {testimonial_id}: {str(e)}", exc_info=True)
            db.session.rollback()
            flash('Failed to update testimonial. Please try again.', 'error')
            return render_template('admin/forms/testimonial_form.html', 
                                 testimonial=testimonial,
                                 title='Edit Testimonial',
                                 form_title='Edit Testimonial',
                                 form_description='Edit this testimonial.',
                                 cancel_url=url_for('main.admin_testimonials'))
    
    return render_template('admin/forms/testimonial_form.html', 
                         testimonial=testimonial,
                         title='Edit Testimonial',
                         form_title='Edit Testimonial',
                         form_description='Edit this testimonial.',
                         cancel_url=url_for('main.admin_testimonials'))


@main_bp.route('/admin/testimonials/<int:testimonial_id>/delete', methods=['POST'])
@login_required
def admin_testimonial_delete(testimonial_id):
    """Delete testimonial."""
    if not current_user.is_admin():
        logger.warning(f"Non-admin user {current_user.id} attempted to delete testimonial {testimonial_id}")
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    testimonial = Testimonial.query.get_or_404(testimonial_id)
    
    try:
        logger.info(f"Deleting testimonial {testimonial_id} (content preview: '{testimonial.content[:50]}...')")
        
        # Store info for logging before deletion
        testimonial_info = {
            'id': testimonial.id,
            'content_preview': testimonial.content[:50] if testimonial.content else 'No content',
            'author_id': testimonial.author_id,
            'was_approved': testimonial.is_approved,
            'was_published': testimonial.is_published
        }
        
        db.session.delete(testimonial)
        db.session.commit()
        
        logger.info(f"Testimonial deleted successfully: {testimonial_info}")
        flash('Testimonial deleted successfully!', 'success')
        
    except Exception as e:
        logger.error(f"Error deleting testimonial {testimonial_id}: {str(e)}", exc_info=True)
        db.session.rollback()
        flash('Failed to delete testimonial. Please try again.', 'error')
    
    return redirect(url_for('main.admin_testimonials'))
