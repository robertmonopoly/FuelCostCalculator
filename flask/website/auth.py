from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError
import re

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not re.match("^[a-zA-Z0-9]{3,16}$", username):
            flash("""Invalid username format, valid usernames are 3-16 characters 
            and only include alphanumeric characters""", category='error')
            return render_template("login.html", user=current_user)

        user = User.query.filter_by(username=username).first()
        if not user:
            flash('Invalid credentials', category='error')
            return render_template("login.html", user=current_user)
        
        if not check_password_hash(user.password, password):
            flash('Invalid credentials', category='error')
            return render_template("login.html", user=current_user)
        
        login_user(user, remember=True)
        return redirect(url_for('views.home'))
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        passwordConfirmation = request.form.get('confirm-password')

        if not re.match("^[a-zA-Z0-9]{3,16}$", username):
            flash("""Invalid username format, valid usernames are 3-16 characters 
            and only include alphanumeric characters""", category='error')
            return render_template("sign_up.html", user=current_user)

        if password != passwordConfirmation:
            flash('The supplied passwords do not match', category='error')
            return render_template("sign_up.html", user=current_user)

        # TODO(Slendy): validate username, hash password on client side rather than server side

        # If someone else already chose this username
        if bool(User.query.filter_by(username=username).first()):
            flash('A user already exists with that username', category='error')
            return render_template("sign_up.html", user=current_user)

        # TODO(Slendy): sha256 is deprecated in Werkzeug 3.0
        new_user = User(username=username, password=generate_password_hash(
        password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        return redirect(url_for('views.home'))
    return render_template("sign_up.html", user=current_user)