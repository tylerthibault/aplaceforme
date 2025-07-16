from flask import Blueprint, render_template, request, flash, redirect, url_for
from datetime import datetime
import logging
from src.models import GodStory
from src import db
from flask_login import login_required, current_user

# Set up logging
logger = logging.getLogger(__name__)

# Create blueprint
god_stories_bp = Blueprint('god_stories', __name__, url_prefix='/admin/god-stories')

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

ALLOWED_VIDEO_TYPES = {
    'video/mp4',
    'video/webm',
    'video/quicktime',
    'video/x-msvideo'
}


@god_stories_bp.route('/')
@login_required
def list_god_stories():
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


@god_stories_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_god_story():
    """Create a new God story."""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        # Get form data
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        status = request.form.get('status', 'draft').strip()
        publish_at = request.form.get('publish_at', '').strip()
        video_file = request.files.get('video_file')
        audio_file = request.files.get('audio_file')
        
        # Log form data received
        logger.info(f"God story creation attempt - Title: {title}, Status: {status}")
        logger.info(f"Form data received: {dict(request.form)}")
        
        # Additional form fields that exist in template but not in model
        author_name = request.form.get('author_name', '').strip()
        category = request.form.get('category', '').strip()
        tags = request.form.get('tags', '').strip()
        bible_references = request.form.get('bible_references', '').strip()
        featured = request.form.get('featured') == 'on'
        allow_comments = request.form.get('allow_comments') == 'on'
        
        # Log additional fields for debugging
        if author_name or category or tags or bible_references or featured or allow_comments:
            logger.warning(f"Extra form fields not stored in model: author_name={author_name}, "
                         f"category={category}, tags={tags}, bible_references={bible_references}, "
                         f"featured={featured}, allow_comments={allow_comments}")
        
        # Validation
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
                errors.append('Publish date is required for scheduled stories')
            else:
                try:
                    parsed_publish_at = datetime.strptime(publish_at, '%Y-%m-%dT%H:%M')
                    if parsed_publish_at <= datetime.now():
                        errors.append('Publish date must be in the future')
                except ValueError:
                    errors.append('Invalid publish date format')
        
        # Validate file uploads
        video_data = None
        audio_data = None
        
        if video_file and video_file.filename:
            if video_file.content_type not in ALLOWED_VIDEO_TYPES:
                errors.append('Invalid video format. Please use MP4, WebM, QuickTime, or AVI.')
            elif len(video_file.read()) > 100 * 1024 * 1024:  # 100MB limit
                errors.append('Video file too large. Maximum size is 100MB.')
            else:
                video_file.seek(0)
                video_data = video_file.read()
                logger.info(f"Video file processed: {len(video_data)} bytes")
            video_file.seek(0)
            
        if audio_file and audio_file.filename:
            if audio_file.content_type not in ALLOWED_AUDIO_TYPES:
                errors.append('Invalid audio format. Please use MP3, WAV, OGG, MP4, M4A, AAC, or FLAC.')
            elif len(audio_file.read()) > 50 * 1024 * 1024:  # 50MB limit
                errors.append('Audio file too large. Maximum size is 50MB.')
            else:
                audio_file.seek(0)
                audio_data = audio_file.read()
                logger.info(f"Audio file processed: {len(audio_data)} bytes")
            audio_file.seek(0)
            
        if errors:
            logger.warning(f"Validation errors found: {errors}")
            for error in errors:
                flash(error, 'error')
            return render_template('admin/forms/god_story_form.html',
                                 title='New God Story',
                                 form_title='Create New God Story',
                                 form_description='Share a testimony of God\'s work.',
                                 cancel_url=url_for('god_stories.list_god_stories'))
        
        try:
            logger.info("Creating new God story object")
            
            # Create new God story with only fields that exist in the model
            god_story = GodStory(
                title=title,
                content=content,
                author_id=current_user.id,
                status=status,
                is_published=(status == 'published'),
                publish_at=parsed_publish_at,
                video_data=video_data,
                audio_data=audio_data
            )
            
            logger.info(f"God story object created successfully: {god_story}")
            
            db.session.add(god_story)
            db.session.commit()
            
            logger.info(f"God story saved to database with ID: {god_story.id}")
            
            flash(f'God story "{title}" created successfully! '
                  f'Fields saved: title, content, author, status, publish_at'
                  f'{", video" if video_data else ""}'
                  f'{", audio" if audio_data else ""}', 'success')
            return redirect(url_for('god_stories.list_god_stories'))
            
        except Exception as e:
            logger.error(f"Error creating God story: {str(e)}")
            db.session.rollback()
            flash('Failed to create God story. Please try again.', 'error')
            return render_template('admin/forms/god_story_form.html',
                                 title='New God Story',
                                 form_title='Create New God Story',
                                 form_description='Share a testimony of God\'s work.',
                                 cancel_url=url_for('god_stories.list_god_stories'))
    
    # GET request
    return render_template('admin/forms/god_story_form.html',
                         title='New God Story',
                         form_title='Create New God Story',
                         form_description='Share a testimony of God\'s work.',
                         cancel_url=url_for('god_stories.list_god_stories'))


@god_stories_bp.route('/<int:story_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_god_story(story_id):
    """Edit an existing God story."""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    god_story = GodStory.query.get_or_404(story_id)
    
    if request.method == 'POST':
        # Get form data
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        status = request.form.get('status', 'draft').strip()
        publish_at = request.form.get('publish_at', '').strip()
        video_file = request.files.get('video_file')
        audio_file = request.files.get('audio_file')
        
        logger.info(f"God story edit attempt - ID: {story_id}, Title: {title}, Status: {status}")
        
        # Validation
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
                errors.append('Publish date is required for scheduled stories')
            else:
                try:
                    parsed_publish_at = datetime.strptime(publish_at, '%Y-%m-%dT%H:%M')
                    if parsed_publish_at <= datetime.now():
                        errors.append('Publish date must be in the future')
                except ValueError:
                    errors.append('Invalid publish date format')
        
        # Validate file uploads (optional for edit)
        video_data = god_story.video_data  # Keep existing by default
        audio_data = god_story.audio_data  # Keep existing by default
        
        if video_file and video_file.filename:
            if video_file.content_type not in ALLOWED_VIDEO_TYPES:
                errors.append('Invalid video format. Please use MP4, WebM, QuickTime, or AVI.')
            elif len(video_file.read()) > 100 * 1024 * 1024:  # 100MB limit
                errors.append('Video file too large. Maximum size is 100MB.')
            else:
                video_file.seek(0)
                video_data = video_file.read()
                logger.info(f"New video file processed: {len(video_data)} bytes")
            video_file.seek(0)
            
        if audio_file and audio_file.filename:
            if audio_file.content_type not in ALLOWED_AUDIO_TYPES:
                errors.append('Invalid audio format. Please use MP3, WAV, OGG, MP4, M4A, AAC, or FLAC.')
            elif len(audio_file.read()) > 50 * 1024 * 1024:  # 50MB limit
                errors.append('Audio file too large. Maximum size is 50MB.')
            else:
                audio_file.seek(0)
                audio_data = audio_file.read()
                logger.info(f"New audio file processed: {len(audio_data)} bytes")
            audio_file.seek(0)
            
        if errors:
            logger.warning(f"Validation errors found: {errors}")
            for error in errors:
                flash(error, 'error')
            return render_template('admin/forms/god_story_form.html',
                                 god_story=god_story,
                                 title='Edit God Story',
                                 form_title='Edit God Story',
                                 form_description='Update this God story.',
                                 cancel_url=url_for('god_stories.list_god_stories'))
        
        try:
            # Update God story
            god_story.title = title
            god_story.content = content
            god_story.status = status
            god_story.is_published = (status == 'published')
            god_story.publish_at = parsed_publish_at
            god_story.video_data = video_data
            god_story.audio_data = audio_data
            god_story.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            logger.info(f"God story {story_id} updated successfully")
            flash(f'God story "{title}" updated successfully!', 'success')
            return redirect(url_for('god_stories.list_god_stories'))
            
        except Exception as e:
            logger.error(f"Error updating God story {story_id}: {str(e)}")
            db.session.rollback()
            flash('Failed to update God story. Please try again.', 'error')
    
    # GET request
    return render_template('admin/forms/god_story_form.html',
                         god_story=god_story,
                         title='Edit God Story',
                         form_title='Edit God Story',
                         form_description='Update this God story.',
                         cancel_url=url_for('god_stories.list_god_stories'))


@god_stories_bp.route('/<int:story_id>/delete', methods=['POST'])
@login_required
def delete_god_story(story_id):
    """Delete a God story."""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    try:
        god_story = GodStory.query.get_or_404(story_id)
        title = god_story.title
        
        logger.info(f"Deleting God story: ID={story_id}, Title='{title}'")
        
        db.session.delete(god_story)
        db.session.commit()
        
        logger.info(f"God story {story_id} deleted successfully")
        flash(f'God story "{title}" has been deleted.', 'success')
        
    except Exception as e:
        logger.error(f"Error deleting God story {story_id}: {str(e)}")
        db.session.rollback()
        flash('Failed to delete God story. Please try again.', 'error')
    
    return redirect(url_for('god_stories.list_god_stories'))
