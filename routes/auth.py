from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models import db
from models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('pages.index'))
    
    if request.method == 'POST':
        # Retrieve form data
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return redirect(url_for('auth.register'))

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('auth.register'))

        # Check existing
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or Email already exists.', 'danger')
            return redirect(url_for('auth.register'))

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        
        # Set a default random avatar
        new_user.avatar_url = f"https://api.dicebear.com/7.x/adventurer/svg?seed={username}"

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('pages.index'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('auth.login'))

        login_user(user, remember=remember)
        
        next_page = request.args.get('next')
        return redirect(next_page or url_for('pages.index'))

    return render_template('auth/login.html')

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            # Under a real app we would mail a token, here we simulate reset.
            flash('A password reset link has been simulated & sent to your email.', 'success')
        else:
            flash('If the email is registered, you will receive a reset link.', 'info')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/forgot_password.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out.', 'info')
    return redirect(url_for('pages.index'))
