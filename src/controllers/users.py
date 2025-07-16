from flask import Blueprint, render_template, request, flash, redirect, url_for
from datetime import datetime
import logging
from src.models import User
from src import db
from flask_login import login_required, current_user

# Set up logging
logger = logging.getLogger(__name__)

# Create blueprint
users_bp = Blueprint('users', __name__, url_prefix='/admin/users')


@users_bp.route('/')
@login_required
def list_users():
    """Display all users for admin management."""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    users = User.query.paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('admin/users.html', 
                         users=users, 
                         pagination=users, 
                         title='Manage Users', 
                         add_url=url_for('users.new_user'))


@users_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_user():
    """Add new user form and handler."""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        # TODO: Implement user creation logic
        logger.info("User creation form submitted")
        flash('User creation not yet implemented.', 'warning')
        return redirect(url_for('users.list_users'))
    
    # TODO: Create user form template
    logger.info("Displaying user creation form")
    flash('User creation form not yet implemented.', 'warning')
    return redirect(url_for('users.list_users'))


@users_bp.route('/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    """Edit user form and handler."""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        # TODO: Implement user edit logic
        logger.info(f"User edit form submitted for user {user_id}")
        flash('User editing not yet implemented.', 'warning')
        return redirect(url_for('users.list_users'))
    
    # TODO: Create user edit form template
    logger.info(f"Displaying user edit form for user {user_id}")
    flash('User editing form not yet implemented.', 'warning')
    return redirect(url_for('users.list_users'))


@users_bp.route('/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    """Delete user."""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    user = User.query.get_or_404(user_id)
    
    # TODO: Implement user deletion logic
    logger.info(f"User deletion attempted for user {user_id}")
    flash('User deletion not yet implemented.', 'warning')
    return redirect(url_for('users.list_users'))
