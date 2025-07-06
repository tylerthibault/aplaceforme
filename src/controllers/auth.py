from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from src.models.user import User
from src import db, bcrypt
from typing import Optional
import re

# Create auth blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle user registration.
    
    Returns:
        Response: Registration form or redirect after successful registration
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')
        
        # Validate inputs
        errors = []
        
        # Username validation
        if not username:
            errors.append('Username is required')
        elif len(username) < 3:
            errors.append('Username must be at least 3 characters long')
        elif len(username) > 80:
            errors.append('Username must be less than 80 characters')
        elif not re.match(r'^[a-zA-Z0-9_]+$', username):
            errors.append('Username can only contain letters, numbers, and underscores')
        
        # Email validation
        if not email:
            errors.append('Email is required')
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            errors.append('Please enter a valid email address')
        
        # Password validation
        if not password:
            errors.append('Password is required')
        elif len(password) < 8:
            errors.append('Password must be at least 8 characters long')
        elif not re.search(r'[A-Za-z]', password):
            errors.append('Password must contain at least one letter')
        elif not re.search(r'[0-9]', password):
            errors.append('Password must contain at least one number')
        
        # Password confirmation
        if password != password_confirm:
            errors.append('Passwords do not match')
        
        # Check for existing users
        if User.query.filter_by(username=username).first():
            errors.append('Username already exists')
        if User.query.filter_by(email=email).first():
            errors.append('Email already registered')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('auth/register.html', username=username, email=email)
        
        # Create new user
        try:
            user = User(
                username=username,
                email=email,
                role='user',
                is_managed=False
            )
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            db.session.rollback()
            flash('Registration failed. Please try again.', 'error')
            return render_template('auth/register.html', username=username, email=email)
    
    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login.
    
    Returns:
        Response: Login form or redirect after successful login
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username_or_email = request.form.get('username_or_email', '').strip()
        password = request.form.get('password', '')
        remember_me = request.form.get('remember_me', False)
        
        if not username_or_email or not password:
            flash('Please enter both username/email and password.', 'error')
            return render_template('auth/login.html', username_or_email=username_or_email)
        
        # Try to find user by username or email
        user = User.query.filter(
            (User.username == username_or_email) | 
            (User.email == username_or_email.lower())
        ).first()
        
        if user and user.check_password(password):
            user.update_last_login()
            db.session.commit()
            
            login_user(user, remember=remember_me)
            
            # Get next page from query parameter
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                flash(f'Welcome back, {user.username}!', 'success')
                return redirect(next_page)
            
            flash(f'Welcome back, {user.username}!', 'success')
            
            # Redirect based on user role
            if user.is_admin():
                return redirect(url_for('main.admin_dashboard'))
            else:
                return redirect(url_for('main.index'))
        else:
            flash('Invalid username/email or password.', 'error')
            return render_template('auth/login.html', username_or_email=username_or_email)
    
    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """
    Handle user logout.
    
    Returns:
        Response: Redirect to home page
    """
    username = current_user.username
    logout_user()
    flash(f'You have been logged out. See you soon, {username}!', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/profile')
@login_required
def profile():
    """
    Display user profile.
    
    Returns:
        Response: User profile page
    """
    return render_template('auth/profile.html', user=current_user)


@auth_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """
    Edit user profile.
    
    Returns:
        Response: Profile edit form or redirect after successful update
    """
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        
        # Validate inputs
        errors = []
        
        # Username validation
        if not username:
            errors.append('Username is required')
        elif len(username) < 3:
            errors.append('Username must be at least 3 characters long')
        elif len(username) > 80:
            errors.append('Username must be less than 80 characters')
        elif not re.match(r'^[a-zA-Z0-9_]+$', username):
            errors.append('Username can only contain letters, numbers, and underscores')
        
        # Email validation
        if not email:
            errors.append('Email is required')
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            errors.append('Please enter a valid email address')
        
        # Check for existing users (excluding current user)
        existing_user = User.query.filter_by(username=username).first()
        if existing_user and existing_user.id != current_user.id:
            errors.append('Username already exists')
        
        existing_email = User.query.filter_by(email=email).first()
        if existing_email and existing_email.id != current_user.id:
            errors.append('Email already registered')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('auth/edit_profile.html', user=current_user)
        
        # Update user
        try:
            current_user.username = username
            current_user.email = email
            db.session.commit()
            
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('auth.profile'))
            
        except Exception as e:
            db.session.rollback()
            flash('Profile update failed. Please try again.', 'error')
            return render_template('auth/edit_profile.html', user=current_user)
    
    return render_template('auth/edit_profile.html', user=current_user)


@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """
    Change user password.
    
    Returns:
        Response: Password change form or redirect after successful change
    """
    if request.method == 'POST':
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validate inputs
        errors = []
        
        if not current_password:
            errors.append('Current password is required')
        elif not current_user.check_password(current_password):
            errors.append('Current password is incorrect')
        
        if not new_password:
            errors.append('New password is required')
        elif len(new_password) < 8:
            errors.append('New password must be at least 8 characters long')
        elif not re.search(r'[A-Za-z]', new_password):
            errors.append('New password must contain at least one letter')
        elif not re.search(r'[0-9]', new_password):
            errors.append('New password must contain at least one number')
        
        if new_password != confirm_password:
            errors.append('New passwords do not match')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('auth/change_password.html')
        
        # Update password
        try:
            current_user.set_password(new_password)
            db.session.commit()
            
            flash('Password changed successfully!', 'success')
            return redirect(url_for('auth.profile'))
            
        except Exception as e:
            db.session.rollback()
            flash('Password change failed. Please try again.', 'error')
            return render_template('auth/change_password.html')
    
    return render_template('auth/change_password.html')
