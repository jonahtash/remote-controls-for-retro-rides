''' API ROUTE IMPLEMENTATION '''

from datetime import date, datetime, timezone
from uuid import uuid4
from flask import request, session, render_template, url_for, redirect, flash, jsonify
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy
from . import app, login_manager, db
from .utils import get_or_create, validate_email, get_display_name, get_elapsed_days, append_to_login_bitfield, do_unlock, do_lock
from .models import Session, User, Interaction, LoginAttempts, RegistrationPIN
import random
import string

MIN_PASSWORD_LENGTH = 8

@login_manager.user_loader
def load_user(user_id):
    """Loads a user based on their id, returning None if they don't exist"""
    return User.query.get(int(user_id))


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    # Return the login template if the user is just GETTING the page
    if request.method == 'GET':
        return render_template('login.html')

    # Otherwise, it's a post request
    # No longer allowed
    flash('Method not allowed', 'error')
    return redirect(url_for('login'))


@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    # Serve the page on a GET request
    if request.method == 'GET':
        return render_template('register.html')

    # Otherwise, handle the POST request to register a new user account
    # Not allowing these anymore
    flash('Method not allowed', 'error')
    return redirect(url_for('register'))

# Page to edit user information
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.route('/makepin', methods=['POST'])
@login_required
def makepin():
    pin = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))
    new_row = RegistrationPIN(pin=pin)
    db.session.add(new_row)
    db.session.commit()
    flash(f'Registration PIN is {pin}', 'message')
    return redirect(url_for('profile'))

@app.route('/delete-account', methods=['POST'])
@login_required
def delete_account():
    email = current_user.email

    # Delete the user information, but maintain their user id
    current_user.delete_identifiable_info()
    logout_user()
    db.session.commit()

    # Reset the session token to prevent the session token from being
    # associated with multiple user accounts
    session['token'] = str(uuid4())

    flash(f'Successfully deleted the account for "{email}"', 'message')
    return redirect(url_for('login'))
@app.route('/unlock_car', methods=['POST'])
@login_required
def unlock_car():
    if do_unlock():
        flash('Doors unlocked', 'message')
        return redirect(url_for('profile'))
    else:
        flash('Unlocking failed', 'error')
        return redirect(url_for('profile'))
@app.route('/lock_car', methods=['POST'])
@login_required
def lock_car():
    if do_lock():
        flash(f'Doors locked', 'message')
        return redirect(url_for('profile'))
    else:
        flash(f'Locking failed', 'error')
        return redirect(url_for('profile'))
