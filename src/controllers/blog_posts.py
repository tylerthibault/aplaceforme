from flask import Blueprint, render_template, request, flash, redirect, url_for
from datetime import datetime
import logging
from src.models import BlogPost
from src import db
from flask_login import login_required, current_user

# Set up logging
logger = logging.getLogger(__name__)

# Create blueprint
blog_posts_bp = Blueprint('blog_posts', __name__, url_prefix='/admin/blog-posts')

# File format constants
ALLOWED_IMAGE_TYPES = {
    'image/jpeg',
    'image/png', 
    'image/gif',
    'image/webp'
}


@blog_posts_bp.route('/')
@login_required
def list_blog_posts():
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


@blog_posts_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_blog_post():
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
                                 cancel_url=url_for('blog_posts.list_blog_posts'))
        
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
            
            flash('Blog post created successfully!', 'success')
            return redirect(url_for('blog_posts.list_blog_posts'))
            
        except Exception as e:
            logger.error(f"Error creating blog post: {str(e)}", exc_info=True)
            db.session.rollback()
            flash('Failed to create blog post. Please try again.', 'error')
            return render_template('admin/forms/blog_post_form.html', 
                                 title='Add New Blog Post',
                                 form_title='Add New Blog Post',
                                 form_description='Create a new blog post.',
                                 cancel_url=url_for('blog_posts.list_blog_posts'))
    
    return render_template('admin/forms/blog_post_form.html', 
                         title='Add New Blog Post',
                         form_title='Add New Blog Post',
                         form_description='Create a new blog post.',
                         cancel_url=url_for('blog_posts.list_blog_posts'))


@blog_posts_bp.route('/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_blog_post(post_id):
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
                                 cancel_url=url_for('blog_posts.list_blog_posts'))
        
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
            return redirect(url_for('blog_posts.list_blog_posts'))
            
        except Exception as e:
            logger.error(f"Error updating blog post {post_id}: {str(e)}", exc_info=True)
            db.session.rollback()
            flash('Failed to update blog post. Please try again.', 'error')
            return render_template('admin/forms/blog_post_form.html', 
                                 blog_post=blog_post,
                                 title='Edit Blog Post',
                                 form_title='Edit Blog Post',
                                 form_description='Edit this blog post.',
                                 cancel_url=url_for('blog_posts.list_blog_posts'))
    
    return render_template('admin/forms/blog_post_form.html', 
                         blog_post=blog_post,
                         title='Edit Blog Post',
                         form_title='Edit Blog Post',
                         form_description='Edit this blog post.',
                         cancel_url=url_for('blog_posts.list_blog_posts'))


@blog_posts_bp.route('/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_blog_post(post_id):
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
    
    return redirect(url_for('blog_posts.list_blog_posts'))
