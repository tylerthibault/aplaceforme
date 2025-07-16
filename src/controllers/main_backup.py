from flask import Blueprint, render_template, request, abort, flash, redirect, url_for
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
        'total_sstories': GodStory.query.count(),
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


# Admin Form Routes
@main_bp.route('/admin/blog-posts/new', methods=['GET', 'POST'])
@login_required
def admin_blog_post_new():
    """Add new blog post form and handler."""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        # TODO: Implement blog post creation
        flash('Blog post creation not yet implemented.', 'info')
        return redirect(url_for('main.admin_blog_posts'))
    
    return render_template('admin/forms/blog_post_form.html', 
                         title='Add New Blog Post',
                         form_title='Add New Blog Post',
                         form_description='Create a new blog post for your site.',
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
        # TODO: Implement blog post editing
        flash('Blog post editing not yet implemented.', 'info')
        return redirect(url_for('main.admin_blog_posts'))
    
    return render_template('admin/forms/blog_post_form.html', 
                         blog_post=blog_post,
                         title='Edit Blog Post',
                         form_title='Edit Blog Post',
                         form_description='Edit this blog post.',
                         cancel_url=url_for('main.admin_blog_posts'))


@main_bp.route('/admin/god-stories/new', methods=['GET', 'POST'])
@login_required
def admin_god_story_new():
    """Add new God story form and handler."""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        status = request.form.get('status', 'draft')
        author_name = request.form.get('author_name', '').strip()
        category = request.form.get('category', '').strip()
        tags = request.form.get('tags', '').strip()
        
        # Handle file uploads
        featured_image = request.files.get('featured_image')
        audio_file = request.files.get('audio_file')
        video_file = request.files.get('video_file')
        
        # Validate inputs
        errors = []
        
        if not title:
            errors.append('Title is required')
        elif len(title) > 200:
            errors.append('Title must be less than 200 characters')
            
        if not content:
            errors.append('Content is required')
            
        # Validate file uploads
        allowed_image_types = {'image/jpeg', 'image/png', 'image/gif', 'image/webp'}
        allowed_audio_types = {'audio/mpeg', 'audio/wav', 'audio/ogg', 'audio/mp4', 'video/mp4', 'audio/x-m4a', 'audio/m4a'}  # Added M4A support
        allowed_video_types = {'video/mp4', 'video/webm', 'video/quicktime', 'video/x-msvideo'}
        
        if featured_image and featured_image.filename:
            if featured_image.content_type not in allowed_image_types:
                errors.append('Invalid image format. Please use JPEG, PNG, GIF, or WebP.')
            elif len(featured_image.read()) > 5 * 1024 * 1024:  # 5MB limit
                errors.append('Image file too large. Maximum size is 5MB.')
            featured_image.seek(0)  # Reset file pointer
            
        if audio_file and audio_file.filename:
            if audio_file.content_type not in allowed_audio_types:
                errors.append('Invalid audio format. Please use MP3, WAV, OGG, MP4, or M4A.')
            elif len(audio_file.read()) > 50 * 1024 * 1024:  # 50MB limit
                errors.append('Audio file too large. Maximum size is 50MB.')
            audio_file.seek(0)  # Reset file pointer
            
        if video_file and video_file.filename:
            if video_file.content_type not in ALLOWED_VIDEO_TYPES:
                errors.append('Invalid video format. Please use MP4, WebM, MOV, or AVI.')
            elif len(video_file.read()) > 100 * 1024 * 1024:  # 100MB limit
                errors.append('Video file too large. Maximum size is 100MB.')
            else:
                # Check if video contains audio
                video_file.seek(0)  # Reset to beginning
                video_data = video_file.read()
                if not check_video_has_audio(video_data):
                    flash('Warning: The uploaded video does not appear to contain audio tracks. Users will only see video without sound.', 'warning')
            video_file.seek(0)  # Reset file pointer
            
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('admin/forms/god_story_form.html', 
                                 title='Add New God Story',
                                 form_title='Add New God Story',
                                 form_description='Share a new story of God\'s faithfulness.',
                                 cancel_url=url_for('main.admin_god_stories'),
                                 god_story_title=title,
                                 god_story_content=content)
        
        # Create new God story
        try:
            god_story = GodStory(
                title=title,
                content=content,
                author_id=current_user.id,
                status=status,
                author_name=author_name if author_name else current_user.username,
                category=category if category else None,
                tags=tags if tags else None
            )
            
            # Handle file data
            if featured_image and featured_image.filename:
                god_story.image_data = featured_image.read()
                
            if audio_file and audio_file.filename:
                god_story.audio_data = audio_file.read()
                
            if video_file and video_file.filename:
                god_story.video_data = video_file.read()
            
            if status == 'published':
                god_story.publish()
            
            db.session.add(god_story)
            db.session.commit()
            
            flash('God story created successfully!', 'success')
            return redirect(url_for('main.admin_god_stories'))
            
        except Exception as e:
            db.session.rollback()
            flash('Failed to create God story. Please try again.', 'error')
            return render_template('admin/forms/god_story_form.html', 
                                 title='Add New God Story',
                                 form_title='Add New God Story',
                                 form_description='Share a new story of God\'s faithfulness.',
                                 cancel_url=url_for('main.admin_god_stories'),
                                 god_story_title=title,
                                 god_story_content=content)
    
    return render_template('admin/forms/god_story_form.html', 
                         title='Add New God Story',
                         form_title='Add New God Story',
                         form_description='Share a new story of God\'s faithfulness.',
                         cancel_url=url_for('main.admin_god_stories'))


@main_bp.route('/admin/god-stories/<int:story_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_god_story_edit(story_id):
    """Edit God story form and handler."""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    god_story = GodStory.query.get_or_404(story_id)
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        status = request.form.get('status', 'draft')
        author_name = request.form.get('author_name', '').strip()
        category = request.form.get('category', '').strip()
        tags = request.form.get('tags', '').strip()
        
        # Handle file uploads
        featured_image = request.files.get('featured_image')
        audio_file = request.files.get('audio_file')
        video_file = request.files.get('video_file')
        
        # Validate inputs
        errors = []
        
        if not title:
            errors.append('Title is required')
        elif len(title) > 200:
            errors.append('Title must be less than 200 characters')
            
        if not content:
            errors.append('Content is required')
            
        # Validate file uploads
        if featured_image and featured_image.filename:
            if featured_image.content_type not in ALLOWED_IMAGE_TYPES:
                errors.append('Invalid image format. Please use JPEG, PNG, GIF, or WebP.')
            elif len(featured_image.read()) > 5 * 1024 * 1024:  # 5MB limit
                errors.append('Image file too large. Maximum size is 5MB.')
            featured_image.seek(0)  # Reset file pointer
            
        if audio_file and audio_file.filename:
            if audio_file.content_type not in ALLOWED_AUDIO_TYPES:
                errors.append('Invalid audio format. Please use MP3, WAV, OGG, MP4, M4A, AAC, or FLAC.')
            elif len(audio_file.read()) > 50 * 1024 * 1024:  # 50MB limit
                errors.append('Audio file too large. Maximum size is 50MB.')
            audio_file.seek(0)  # Reset file pointer
            
        if video_file and video_file.filename:
            if video_file.content_type not in ALLOWED_VIDEO_TYPES:
                errors.append('Invalid video format. Please use MP4, WebM, MOV, or AVI.')
            elif len(video_file.read()) > 100 * 1024 * 1024:  # 100MB limit
                errors.append('Video file too large. Maximum size is 100MB.')
            else:
                # Check if video contains audio
                video_file.seek(0)  # Reset to beginning
                video_data = video_file.read()
                if not check_video_has_audio(video_data):
                    flash('Warning: The uploaded video does not appear to contain audio tracks. Users will only see video without sound.', 'warning')
            video_file.seek(0)  # Reset file pointer
            
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('admin/forms/god_story_form.html', 
                                 god_story=god_story,
                                 title='Edit God Story',
                                 form_title='Edit God Story',
                                 form_description='Edit this God story.',
                                 cancel_url=url_for('main.admin_god_stories'))
        
        # Update God story
        try:
            god_story.title = title
            god_story.content = content
            god_story.status = status
            god_story.author_name = author_name if author_name else current_user.username
            god_story.category = category if category else None
            god_story.tags = tags if tags else None
            
            # Handle file data updates
            if featured_image and featured_image.filename:
                god_story.image_data = featured_image.read()
                
            if audio_file and audio_file.filename:
                god_story.audio_data = audio_file.read()
                
            if video_file and video_file.filename:
                god_story.video_data = video_file.read()
            
            if status == 'published' and not god_story.is_published:
                god_story.publish()
            elif status == 'draft' and god_story.is_published:
                god_story.unpublish()
            
            db.session.commit()
            
            flash('God story updated successfully!', 'success')
            return redirect(url_for('main.admin_god_stories'))
            
        except Exception as e:
            db.session.rollback()
            flash('Failed to update God story. Please try again.', 'error')
            return render_template('admin/forms/god_story_form.html', 
                                 god_story=god_story,
                                 title='Edit God Story',
                                 form_title='Edit God Story',
                                 form_description='Edit this God story.',
                                 cancel_url=url_for('main.admin_god_stories'))
    
    return render_template('admin/forms/god_story_form.html', 
                         god_story=god_story,
                         title='Edit God Story',
                         form_title='Edit God Story',
                         form_description='Edit this God story.',
                         cancel_url=url_for('main.admin_god_stories'))


@main_bp.route('/admin/songs/new', methods=['GET', 'POST'])
@login_required
def admin_song_new():
    """Add new song form and handler."""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        artist = request.form.get('artist', '').strip()
        album = request.form.get('album', '').strip()
        description = request.form.get('description', '').strip()
        genre = request.form.get('genre', '').strip()
        duration = request.form.get('duration', '').strip()
        status = request.form.get('status', 'draft')
        
        # Handle file uploads
        audio_file = request.files.get('audio_file')
        cover_image = request.files.get('cover_image')
        
        # Validate inputs
        errors = []
        
        if not title:
            errors.append('Title is required')
        elif len(title) > 200:
            errors.append('Title must be less than 200 characters')
            
        if not audio_file or not audio_file.filename:
            errors.append('Audio file is required')
            
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
            
        # Validate file uploads
        if audio_file and audio_file.filename:
            if audio_file.content_type not in ALLOWED_AUDIO_TYPES:
                errors.append('Invalid audio format. Please use MP3, WAV, OGG, MP4, M4A, AAC, or FLAC.')
            elif len(audio_file.read()) > 50 * 1024 * 1024:  # 50MB limit
                errors.append('Audio file too large. Maximum size is 50MB.')
            audio_file.seek(0)  # Reset file pointer
            
        if cover_image and cover_image.filename:
            if cover_image.content_type not in ALLOWED_IMAGE_TYPES:
                errors.append('Invalid image format. Please use JPEG, PNG, GIF, or WebP.')
            elif len(cover_image.read()) > 5 * 1024 * 1024:  # 5MB limit
                errors.append('Image file too large. Maximum size is 5MB.')
            cover_image.seek(0)  # Reset file pointer
            
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('admin/forms/song_form.html', 
                                 title='Add New Song',
                                 form_title='Add New Song',
                                 form_description='Upload a new song to your collection.',
                                 cancel_url=url_for('main.admin_songs'),
                                 song_title=title,
                                 song_artist=artist,
                                 song_album=album,
                                 song_description=description)
        
        # Create new song
        try:
            song = Song(
                title=title,
                artist=artist if artist else None,
                album=album if album else None,
                description=description if description else None,
                genre=genre if genre else None,
                duration=duration,
                uploaded_by=current_user.id,
                status=status
            )
            
            # Handle file data
            if audio_file and audio_file.filename:
                song.file_data = audio_file.read()
                
            if cover_image and cover_image.filename:
                song.cover_image_data = cover_image.read()
            
            if status == 'published':
                song.publish()
            
            db.session.add(song)
            db.session.commit()
            
            flash('Song uploaded successfully!', 'success')
            return redirect(url_for('main.admin_songs'))
            
        except Exception as e:
            db.session.rollback()
            flash('Failed to upload song. Please try again.', 'error')
            return render_template('admin/forms/song_form.html', 
                                 title='Add New Song',
                                 form_title='Add New Song',
                                 form_description='Upload a new song to your collection.',
                                 cancel_url=url_for('main.admin_songs'),
                                 song_title=title,
                                 song_artist=artist,
                                 song_album=album,
                                 song_description=description)
    
    return render_template('admin/forms/song_form.html', 
                         title='Add New Song',
                         form_title='Add New Song',
                         form_description='Upload a new song to your collection.',
                         cancel_url=url_for('main.admin_songs'))


@main_bp.route('/admin/songs/<int:song_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_song_edit(song_id):
    """Edit song form and handler."""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    song = Song.query.get_or_404(song_id)
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        artist = request.form.get('artist', '').strip()
        album = request.form.get('album', '').strip()
        description = request.form.get('description', '').strip()
        genre = request.form.get('genre', '').strip()
        duration = request.form.get('duration', '').strip()
        status = request.form.get('status', 'draft')
        
        # Handle file uploads
        audio_file = request.files.get('audio_file')
        cover_image = request.files.get('cover_image')
        
        # Validate inputs
        errors = []
        
        if not title:
            errors.append('Title is required')
        elif len(title) > 200:
            errors.append('Title must be less than 200 characters')
            
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
            
        # Validate file uploads
        if audio_file and audio_file.filename:
            if audio_file.content_type not in ALLOWED_AUDIO_TYPES:
                errors.append('Invalid audio format. Please use MP3, WAV, OGG, MP4, M4A, AAC, or FLAC.')
            elif len(audio_file.read()) > 50 * 1024 * 1024:  # 50MB limit
                errors.append('Audio file too large. Maximum size is 50MB.')
            audio_file.seek(0)  # Reset file pointer
            
        if cover_image and cover_image.filename:
            if cover_image.content_type not in ALLOWED_IMAGE_TYPES:
                errors.append('Invalid image format. Please use JPEG, PNG, GIF, or WebP.')
            elif len(cover_image.read()) > 5 * 1024 * 1024:  # 5MB limit
                errors.append('Image file too large. Maximum size is 5MB.')
            cover_image.seek(0)  # Reset file pointer
            
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('admin/forms/song_form.html', 
                                 song=song,
                                 title='Edit Song',
                                 form_title='Edit Song',
                                 form_description='Edit this song.',
                                 cancel_url=url_for('main.admin_songs'))
        
        # Update song
        try:
            song.title = title
            song.artist = artist if artist else None
            song.album = album if album else None
            song.description = description if description else None
            song.genre = genre if genre else None
            song.duration = duration
            song.status = status
            
            # Handle file data updates
            if audio_file and audio_file.filename:
                song.file_data = audio_file.read()
                
            if cover_image and cover_image.filename:
                song.cover_image_data = cover_image.read()
            
            if status == 'published' and not song.is_published:
                song.publish()
            elif status == 'draft' and song.is_published:
                song.unpublish()
            
            db.session.commit()
            
            flash('Song updated successfully!', 'success')
            return redirect(url_for('main.admin_songs'))
            
        except Exception as e:
            db.session.rollback()
            flash('Failed to update song. Please try again.', 'error')
            return render_template('admin/forms/song_form.html', 
                                 song=song,
                                 title='Edit Song',
                                 form_title='Edit Song',
                                 form_description='Edit this song.',
                                 cancel_url=url_for('main.admin_songs'))
    
    return render_template('admin/forms/song_form.html', 
                         song=song,
                         title='Edit Song',
                         form_title='Edit Song',
                         form_description='Edit this song.',
                         cancel_url=url_for('main.admin_songs'))


@main_bp.route('/admin/testimonials/new', methods=['GET', 'POST'])
@login_required
def admin_testimonial_new():
    """Add new testimonial form and handler."""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        # TODO: Implement testimonial creation
        flash('Testimonial creation not yet implemented.', 'info')
        return redirect(url_for('main.admin_testimonials'))
    
    return render_template('admin/forms/testimonial_form.html', 
                         title='Add New Testimonial',
                         form_title='Add New Testimonial',
                         form_description='Share a new testimonial.',
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
        # TODO: Implement testimonial editing
        flash('Testimonial editing not yet implemented.', 'info')
        return redirect(url_for('main.admin_testimonials'))
    
    return render_template('admin/forms/testimonial_form.html', 
                         testimonial=testimonial,
                         title='Edit Testimonial',
                         form_title='Edit Testimonial',
                         form_description='Edit this testimonial.',
                         cancel_url=url_for('main.admin_testimonials'))


# User and admin management routes for new/edit functionality will be added here later
@main_bp.route('/admin/users/new', methods=['GET', 'POST'])
@login_required
def admin_user_new():
    """Add new user form and handler."""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        # TODO: Implement user creation
        flash('User creation not yet implemented.', 'info')
        return redirect(url_for('main.admin_users'))
    
    return render_template('admin/forms/user_form.html', 
                         title='Add New User',
                         form_title='Add New User',
                         form_description='Create a new user account.',
                         cancel_url=url_for('main.admin_users'))


@main_bp.route('/admin/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_user_edit(user_id):
    """Edit user form and handler."""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        # TODO: Implement user editing
        flash('User editing not yet implemented.', 'info')
        return redirect(url_for('main.admin_users'))
    
    return render_template('admin/forms/user_form.html', 
                         user=user,
                         title='Edit User',
                         form_title='Edit User',
                         form_description='Edit this user account.',
                         cancel_url=url_for('main.admin_users'))


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
    from flask import Response
    
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
    from flask import Response
    
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
    from flask import Response
    
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
    from flask import Response
    
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