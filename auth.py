from . import db, qrcode
from .models import User
from binascii import hexlify
import os
import uuid
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

class chall_context:
    def __init__(self, id, challenge):
        self.id = id
        self.challenge = challenge
    def to_string(self):
        chall = str(self.challenge)
        chall = chall[2:len(chall)-1]
        return '{ "id":' + str(self.id) + ', "challenge":' + chall + ' }'

class signup_context:
    def __init__(self, id, url):
        self.id = id
        self.url = url
    def to_string(self):
        url = self.url
        return '{ "id":' + str(self.id) + ', "url":' + url + ' }'

@auth.route('/login')
def login():
    if current_user.is_authenticated:
        redirect('main.profile')
    return render_template('login.html',
        content = chall_context(uuid.uuid4(), hexlify(os.urandom(32))).to_string(),
        next=request.args.get('next')
    )

@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(usr=username).first()

    if not user or not check_password_hash(user.pub, password):
        flash('Username or password incorrect')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirectp_dest(url_for('main.profile'))

@auth.route('/signup')
def signup():
    if current_user.is_authenticated:
        redirect('main.profile')
    return render_template('signup.html', content=signup_context(uuid.uuid4(), request.base_url).to_string())

@auth.route('/signup', methods=['POST'])
def signup_post():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(usr=username).first()

    if user:
        flash('Username already exists')
        return redirect(url_for('auth.signup'))

    new_user = User(usr=username, pub=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))