from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

def redirectp_dest(fallback):
    dest = request.form.get('next')
    try:
        return redirect(url_for(dest))
    except:
        return redirect(fallback)

@auth.route('/login')
def login():
    if current_user.is_authenticated:
        redirect('main.profile')
    return render_template('login.html', next=request.args.get('next'))


@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        flash('Username or password incorrect')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirectp_dest(url_for('main.profile'))

@auth.route('/signup')
def signup():
    if current_user.is_authenticated:
        redirect('main.profile')
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    return ""

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))