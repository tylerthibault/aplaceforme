from flask import Blueprint, render_template, request, flash, redirect, url_for
from datetime import datetime
import logging
from src.models import Song
from src import db
from flask_login import login_required, current_user

# Set up logging
logger = logging.getLogger(__name__)

# Create blueprint
songs_bp = Blueprint('songs', __name__, url_prefix='/admin/songs')

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


@songs_bp.route('/')
@login_required
def list_songs():
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


@songs_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_song():
    """Create a new song."""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        # Get form data
        title = request.form.get('title', '').strip()
        artist = request.form.get('artist', '').strip()
        description = request.form.get('description', '').strip()
        status = request.form.get('status', 'draft').strip()
        publish_at = request.form.get('publish_at', '').strip()
        audio_file = request.files.get('audio_file')
        
        # Log form data received
        logger.info(f"Song creation attempt - Title: {title}, Artist: {artist}, Status: {status}")
        logger.info(f"Form data received: {dict(request.form)}")
        
        # Additional form fields that exist in template but not in model
        album = request.form.get('album', '').strip()
        genre = request.form.get('genre', '').strip()
        year = request.form.get('year', '').strip()
        duration = request.form.get('duration', '').strip()
        featured = request.form.get('featured') == 'on'
        allow_download = request.form.get('allow_download') == 'on'
        
        # Log additional fields for debugging
        if album or genre or year or duration or featured or allow_download:
            logger.warning(f"Extra form fields not stored in model: album={album}, "
                         f"genre={genre}, year={year}, duration={duration}, "
                         f"featured={featured}, allow_download={allow_download}")
        
        # Validation
        errors = []
        logger.info("Starting form validation")
        
        if not title:
            errors.append('Title is required')
        elif len(title) > 200:
            errors.append('Title must be less than 200 characters')
            
        if not artist:
            errors.append('Artist is required')
        elif len(artist) > 100:
            errors.append('Artist name must be less than 100 characters')
            
        # Audio file is required for songs
        if not audio_file or not audio_file.filename:
            errors.append('Audio file is required')
            
        # Validate publish date for scheduled status
        parsed_publish_at = None
        if status == 'scheduled':
            if not publish_at:
                errors.append('Publish date is required for scheduled songs')
            else:
                try:
                    parsed_publish_at = datetime.strptime(publish_at, '%Y-%m-%dT%H:%M')
                    if parsed_publish_at <= datetime.now():
                        errors.append('Publish date must be in the future')
                except ValueError:
                    errors.append('Invalid publish date format')
        
        # Validate audio file upload
        audio_data = None
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
            return render_template('admin/forms/song_form.html',
                                 title='New Song',
                                 form_title='Add New Song',
                                 form_description='Upload a new song to your music library.',
                                 cancel_url=url_for('songs.list_songs'))
        
        try:
            logger.info("Creating new song object")
            
            # Create new song with only fields that exist in the model
            song = Song(
                title=title,
                artist=artist,
                description=description,
                file_data=audio_data,
                uploaded_by=current_user.id,
                status=status,
                is_published=(status == 'published'),
                publish_at=parsed_publish_at
            )
            
            logger.info(f"Song object created successfully: {song}")
            
            db.session.add(song)
            db.session.commit()
            
            logger.info(f"Song saved to database with ID: {song.id}")
            
            flash(f'Song "{title}" by {artist} created successfully! '
                  f'Fields saved: title, artist, description, audio file, status, publish_at', 'success')
            return redirect(url_for('songs.list_songs'))
            
        except Exception as e:
            logger.error(f"Error creating song: {str(e)}")
            db.session.rollback()
            flash('Failed to create song. Please try again.', 'error')
            return render_template('admin/forms/song_form.html',
                                 title='New Song',
                                 form_title='Add New Song',
                                 form_description='Upload a new song to your music library.',
                                 cancel_url=url_for('songs.list_songs'))
    
    # GET request
    return render_template('admin/forms/song_form.html',
                         title='New Song',
                         form_title='Add New Song',
                         form_description='Upload a new song to your music library.',
                         cancel_url=url_for('songs.list_songs'))


@songs_bp.route('/<int:song_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_song(song_id):
    """Edit an existing song."""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    song = Song.query.get_or_404(song_id)
    
    if request.method == 'POST':
        # Get form data
        title = request.form.get('title', '').strip()
        artist = request.form.get('artist', '').strip()
        description = request.form.get('description', '').strip()
        status = request.form.get('status', 'draft').strip()
        publish_at = request.form.get('publish_at', '').strip()
        audio_file = request.files.get('audio_file')
        
        logger.info(f"Song edit attempt - ID: {song_id}, Title: {title}, Artist: {artist}")
        
        # Validation
        errors = []
        
        if not title:
            errors.append('Title is required')
        elif len(title) > 200:
            errors.append('Title must be less than 200 characters')
            
        if not artist:
            errors.append('Artist is required')
        elif len(artist) > 100:
            errors.append('Artist name must be less than 100 characters')
            
        # Validate publish date for scheduled status
        parsed_publish_at = None
        if status == 'scheduled':
            if not publish_at:
                errors.append('Publish date is required for scheduled songs')
            else:
                try:
                    parsed_publish_at = datetime.strptime(publish_at, '%Y-%m-%dT%H:%M')
                    if parsed_publish_at <= datetime.now():
                        errors.append('Publish date must be in the future')
                except ValueError:
                    errors.append('Invalid publish date format')
        
        # Validate audio file upload (optional for edit)
        audio_data = song.file_data  # Keep existing by default
        
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
            return render_template('admin/forms/song_form.html',
                                 song=song,
                                 title='Edit Song',
                                 form_title='Edit Song',
                                 form_description='Update this song.',
                                 cancel_url=url_for('songs.list_songs'))
        
        try:
            # Update song
            song.title = title
            song.artist = artist
            song.description = description
            song.file_data = audio_data
            song.status = status
            song.is_published = (status == 'published')
            song.publish_at = parsed_publish_at
            song.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            logger.info(f"Song {song_id} updated successfully")
            flash(f'Song "{title}" by {artist} updated successfully!', 'success')
            return redirect(url_for('songs.list_songs'))
            
        except Exception as e:
            logger.error(f"Error updating song {song_id}: {str(e)}")
            db.session.rollback()
            flash('Failed to update song. Please try again.', 'error')
    
    # GET request
    return render_template('admin/forms/song_form.html',
                         song=song,
                         title='Edit Song',
                         form_title='Edit Song',
                         form_description='Update this song.',
                         cancel_url=url_for('songs.list_songs'))


@songs_bp.route('/<int:song_id>/delete', methods=['POST'])
@login_required
def delete_song(song_id):
    """Delete a song."""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    try:
        song = Song.query.get_or_404(song_id)
        title = song.title
        artist = song.artist
        
        logger.info(f"Deleting song: ID={song_id}, Title='{title}' by {artist}")
        
        db.session.delete(song)
        db.session.commit()
        
        logger.info(f"Song {song_id} deleted successfully")
        flash(f'Song "{title}" by {artist} has been deleted.', 'success')
        
    except Exception as e:
        logger.error(f"Error deleting song {song_id}: {str(e)}")
        db.session.rollback()
        flash('Failed to delete song. Please try again.', 'error')
    
    return redirect(url_for('songs.list_songs'))
