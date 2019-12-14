from . import db, login_manager
from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@login_manager.unauthorized_handler
def handle_needs_login():
    flash("You have to be logged in to access this page.")
    return redirect(url_for('auth.login', next=request.endpoint))

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.usr)
