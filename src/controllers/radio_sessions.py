from flask import Blueprint, render_template, request, flash, redirect, url_for
from datetime import datetime
import logging
from src.models import RadioSession
from src import db
from flask_login import login_required, current_user

# Set up logging
logger = logging.getLogger(__name__)

# Create blueprint
radio_sessions_bp = Blueprint('radio_sessions', __name__, url_prefix='/admin/radio-sessions')

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


@radio_sessions_bp.route('/')
@login_required
def list_radio_sessions():
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


@radio_sessions_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_radio_session():
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
                                 cancel_url=url_for('radio_sessions.list_radio_sessions'))
        
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
            
            flash('Radio session created successfully!', 'success')
            return redirect(url_for('radio_sessions.list_radio_sessions'))
            
        except Exception as e:
            logger.error(f"Error creating radio session: {str(e)}", exc_info=True)
            db.session.rollback()
            logger.info("Database session rolled back")
            flash('Failed to create radio session. Please try again.', 'error')
            return render_template('admin/forms/radio_session_form.html', 
                                 title='Add New Radio Session',
                                 form_title='Add New Radio Session',
                                 form_description='Create a new radio episode.',
                                 cancel_url=url_for('radio_sessions.list_radio_sessions'))
    
    return render_template('admin/forms/radio_session_form.html', 
                         title='Add New Radio Session',
                         form_title='Add New Radio Session',
                         form_description='Create a new radio episode.',
                         cancel_url=url_for('radio_sessions.list_radio_sessions'))


@radio_sessions_bp.route('/<int:session_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_radio_session(session_id):
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
                                 cancel_url=url_for('radio_sessions.list_radio_sessions'))
        
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
            return redirect(url_for('radio_sessions.list_radio_sessions'))
            
        except Exception as e:
            db.session.rollback()
            flash('Failed to update radio session. Please try again.', 'error')
            return render_template('admin/forms/radio_session_form.html', 
                                 radio_session=radio_session,
                                 title='Edit Radio Session',
                                 form_title='Edit Radio Session',
                                 form_description='Edit this radio session.',
                                 cancel_url=url_for('radio_sessions.list_radio_sessions'))
    
    return render_template('admin/forms/radio_session_form.html', 
                         radio_session=radio_session,
                         title='Edit Radio Session',
                         form_title='Edit Radio Session',
                         form_description='Edit this radio session.',
                         cancel_url=url_for('radio_sessions.list_radio_sessions'))


@radio_sessions_bp.route('/<int:session_id>/delete', methods=['POST'])
@login_required
def delete_radio_session(session_id):
    """Delete radio session."""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    radio_session = RadioSession.query.get_or_404(session_id)
    
    try:
        logger.info(f"Deleting radio session {session_id}: '{radio_session.title}'")
        db.session.delete(radio_session)
        db.session.commit()
        logger.info(f"Radio session {session_id} deleted successfully")
        flash('Radio session deleted successfully!', 'success')
    except Exception as e:
        logger.error(f"Error deleting radio session {session_id}: {str(e)}", exc_info=True)
        db.session.rollback()
        flash('Failed to delete radio session. Please try again.', 'error')
    
    return redirect(url_for('radio_sessions.list_radio_sessions'))
