from flask import Blueprint, render_template, request, flash, redirect, url_for
from datetime import datetime
import logging
from src.models import Testimonial
from src import db
from flask_login import login_required, current_user

# Set up logging
logger = logging.getLogger(__name__)

# Create blueprint
testimonials_bp = Blueprint('testimonials', __name__, url_prefix='/admin/testimonials')

# File format constants
ALLOWED_IMAGE_TYPES = {
    'image/jpeg',
    'image/png', 
    'image/gif',
    'image/webp'
}


@testimonials_bp.route('/')
@login_required
def list_testimonials():
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


@testimonials_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_testimonial():
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
                                 cancel_url=url_for('testimonials.list_testimonials'))
        
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
            
            flash('Testimonial created successfully!', 'success')
            return redirect(url_for('testimonials.list_testimonials'))
            
        except ValueError as ve:
            logger.error(f"Validation error creating testimonial: {str(ve)}")
            db.session.rollback()
            flash(str(ve), 'error')
            return render_template('admin/forms/testimonial_form.html', 
                                 title='Add New Testimonial',
                                 form_title='Add New Testimonial',
                                 form_description='Create a new testimonial.',
                                 cancel_url=url_for('testimonials.list_testimonials'))
        except Exception as e:
            logger.error(f"Error creating testimonial: {str(e)}", exc_info=True)
            db.session.rollback()
            logger.info("Database session rolled back")
            flash('Failed to create testimonial. Please try again.', 'error')
            return render_template('admin/forms/testimonial_form.html', 
                                 title='Add New Testimonial',
                                 form_title='Add New Testimonial',
                                 form_description='Create a new testimonial.',
                                 cancel_url=url_for('testimonials.list_testimonials'))
    
    return render_template('admin/forms/testimonial_form.html', 
                         title='Add New Testimonial',
                         form_title='Add New Testimonial',
                         form_description='Create a new testimonial.',
                         cancel_url=url_for('testimonials.list_testimonials'))


@testimonials_bp.route('/<int:testimonial_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_testimonial(testimonial_id):
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
                                 cancel_url=url_for('testimonials.list_testimonials'))
        
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
            return redirect(url_for('testimonials.list_testimonials'))
            
        except ValueError as ve:
            logger.error(f"Validation error updating testimonial {testimonial_id}: {str(ve)}")
            db.session.rollback()
            flash(str(ve), 'error')
            return render_template('admin/forms/testimonial_form.html', 
                                 testimonial=testimonial,
                                 title='Edit Testimonial',
                                 form_title='Edit Testimonial',
                                 form_description='Edit this testimonial.',
                                 cancel_url=url_for('testimonials.list_testimonials'))
        except Exception as e:
            logger.error(f"Error updating testimonial {testimonial_id}: {str(e)}", exc_info=True)
            db.session.rollback()
            flash('Failed to update testimonial. Please try again.', 'error')
            return render_template('admin/forms/testimonial_form.html', 
                                 testimonial=testimonial,
                                 title='Edit Testimonial',
                                 form_title='Edit Testimonial',
                                 form_description='Edit this testimonial.',
                                 cancel_url=url_for('testimonials.list_testimonials'))
    
    return render_template('admin/forms/testimonial_form.html', 
                         testimonial=testimonial,
                         title='Edit Testimonial',
                         form_title='Edit Testimonial',
                         form_description='Edit this testimonial.',
                         cancel_url=url_for('testimonials.list_testimonials'))


@testimonials_bp.route('/<int:testimonial_id>/delete', methods=['POST'])
@login_required
def delete_testimonial(testimonial_id):
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
    
    return redirect(url_for('testimonials.list_testimonials'))
