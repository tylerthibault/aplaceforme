from flask import Blueprint, render_template, request, abort, flash, redirect, url_for
from typing import Tuple
from src.models import BlogPost, GodStory, Song, Testimonial, RadioSession, User
from src import db
from flask_login import login_required, current_user

# Create main blueprint
main_bp = Blueprint('main', __name__)


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
        allowed_audio_types = {'audio/mpeg', 'audio/wav', 'audio/ogg', 'audio/mp4'}
        allowed_video_types = {'video/mp4', 'video/webm', 'video/quicktime', 'video/x-msvideo'}
        
        if featured_image and featured_image.filename:
            if featured_image.content_type not in allowed_image_types:
                errors.append('Invalid image format. Please use JPEG, PNG, GIF, or WebP.')
            elif len(featured_image.read()) > 5 * 1024 * 1024:  # 5MB limit
                errors.append('Image file too large. Maximum size is 5MB.')
            featured_image.seek(0)  # Reset file pointer
            
        if audio_file and audio_file.filename:
            if audio_file.content_type not in allowed_audio_types:
                errors.append('Invalid audio format. Please use MP3, WAV, OGG, or M4A.')
            elif len(audio_file.read()) > 50 * 1024 * 1024:  # 50MB limit
                errors.append('Audio file too large. Maximum size is 50MB.')
            audio_file.seek(0)  # Reset file pointer
            
        if video_file and video_file.filename:
            if video_file.content_type not in allowed_video_types:
                errors.append('Invalid video format. Please use MP4, WebM, MOV, or AVI.')
            elif len(video_file.read()) > 100 * 1024 * 1024:  # 100MB limit
                errors.append('Video file too large. Maximum size is 100MB.')
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
        allowed_image_types = {'image/jpeg', 'image/png', 'image/gif', 'image/webp'}
        allowed_audio_types = {'audio/mpeg', 'audio/wav', 'audio/ogg', 'audio/mp4'}
        allowed_video_types = {'video/mp4', 'video/webm', 'video/quicktime', 'video/x-msvideo'}
        
        if featured_image and featured_image.filename:
            if featured_image.content_type not in allowed_image_types:
                errors.append('Invalid image format. Please use JPEG, PNG, GIF, or WebP.')
            elif len(featured_image.read()) > 5 * 1024 * 1024:  # 5MB limit
                errors.append('Image file too large. Maximum size is 5MB.')
            featured_image.seek(0)  # Reset file pointer
            
        if audio_file and audio_file.filename:
            if audio_file.content_type not in allowed_audio_types:
                errors.append('Invalid audio format. Please use MP3, WAV, OGG, or M4A.')
            elif len(audio_file.read()) > 50 * 1024 * 1024:  # 50MB limit
                errors.append('Audio file too large. Maximum size is 50MB.')
            audio_file.seek(0)  # Reset file pointer
            
        if video_file and video_file.filename:
            if video_file.content_type not in allowed_video_types:
                errors.append('Invalid video format. Please use MP4, WebM, MOV, or AVI.')
            elif len(video_file.read()) > 100 * 1024 * 1024:  # 100MB limit
                errors.append('Video file too large. Maximum size is 100MB.')
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
        # TODO: Implement song creation
        flash('Song creation not yet implemented.', 'info')
        return redirect(url_for('main.admin_songs'))
    
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
        # TODO: Implement song editing
        flash('Song editing not yet implemented.', 'info')
        return redirect(url_for('main.admin_songs'))
    
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


@main_bp.route('/admin/radio-sessions/new', methods=['GET', 'POST'])
@login_required
def admin_radio_session_new():
    """Add new radio session form and handler."""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        # TODO: Implement radio session creation
        flash('Radio session creation not yet implemented.', 'info')
        return redirect(url_for('main.admin_radio_sessions'))
    
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
        # TODO: Implement radio session editing
        flash('Radio session editing not yet implemented.', 'info')
        return redirect(url_for('main.admin_radio_sessions'))
    
    return render_template('admin/forms/radio_session_form.html', 
                         radio_session=radio_session,
                         title='Edit Radio Session',
                         form_title='Edit Radio Session',
                         form_description='Edit this radio session.',
                         cancel_url=url_for('main.admin_radio_sessions'))


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


# Error handlers
@main_bp.errorhandler(404)
def not_found_error(error) -> Tuple[str, int]:
    """
    Handle 404 errors.
    
    Args:
        error: The error object
        
    Returns:
        Tuple[str, int]: 404 error page template and status code
    """
    return render_template('errors/404.html'), 404


@main_bp.errorhandler(500)
def internal_error(error) -> Tuple[str, int]:
    """
    Handle 500 errors.
    
    Args:
        error: The error object
        
    Returns:
        Tuple[str, int]: 500 error page template and status code
    """
    return render_template('errors/500.html'), 500
