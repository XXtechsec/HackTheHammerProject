from . import db
from .models import User

import os
import uuid
import base64

from flask_login import login_user, logout_user, login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, request, flash, session

from expiringdict import ExpiringDict

auth = Blueprint('auth', __name__)

user_cache = ExpiringDict(max_len=100, max_age_seconds=120)

def redirectp_dest(fallback):
    dest = request.form.get('next')
    try:
        return redirect(url_for(dest))
    except:
        return redirect(fallback)

class chall_context:
    def __init__(self, id, url, challenge):
        self.id = id
        self.challenge = challenge
        self.url = url + "/put"
    def to_string(self):
        return '{ "id":' + str(self.id) + ', "challenge":' + f'"{ self.challenge }"' + ', "url":' + str(self.url) + ' }'

class signup_context:
    def __init__(self, id, url):
        self.id = id
        self.url = url + "/put"
    def to_string(self):
        return '{ "id":' + str(self.id) + ', "url":' + str(self.url) + ' }'

@auth.route('/login')
def login():
    return render_template('login.html', next = request.args.get('next'))

@auth.route('/login', methods=['POST'])
def login_post():
    id = str(uuid.uuid4())
    session["uuid"] = id
    # Insert into cache
    user_cache[id] = {"auth": False, "pub": None, "challenge": None}
    # Get pub key
    user = User.query.filter_by(usr=request.form.get('username')).first()
    # But don't say anything if user does not exist
    if user:
        user_cache[id]["pub"] = user.pub
    return redirect(url_for('auth.login_next'))

@auth.route('/login/next')
def login_next():
    if current_user.is_authenticated:
        redirect('main.profile')
    id = session.get("uuid", None)
    if id is None or id not in user_cache:
        return redirect(url_for('auth.login'))
    # Insert into cache
    chall = base64.b64encode(os.urandom(32))
    user_cache[id]["challenge"] = chall
    print(user_cache[id])
    # Get obj str
    str = chall_context(id, request.base_url, chall).to_string()
    print(str)
    return render_template('loginqr.html', content = str, next = request.args.get('next'), remember = request.args.get('remember'))

@auth.route('/login/next', methods=['POST'])
def login_next_post():
    id = session.get("uuid", None)
    remember = True if request.form.get('remember') else False
    if id in user_cache and user_cache[id]["auth"] == True:
        user = User.query.filter_by(pub=user_cache[id]["pub"]).first()
        if user:
            login_user(user, remember=remember)
            flash('Login success!')
            return redirect(url_for('auth.login_next'))
    flash('Login authentication failed...')
    return redirect(url_for('auth.login_next'))

@auth.route('/login/next/put', methods=['POST'])
def login_next_put():
    id = request.form.get('uuid')
    pub = base64.b64decode(request.form.get('pub')).decode("utf-8")
    sig = base64.b64decode(request.form.get('sig'))
    print(pub)
    if id in user_cache and user_cache[id]["pub"] == pub:
        print("OK")
        from PKE import DSS
        user_cache[id]["auth"] = DSS.verify_signature(user_cache[id]["challenge"], sig, pub)
        print(user_cache[id]["auth"])
    return redirect(url_for('auth.login'))

@auth.route('/signup')
def signup():
    if current_user.is_authenticated:
        redirect('main.profile')
    return render_template('signup.html', content=signup_context(uuid.uuid4(), request.base_url).to_string())

@auth.route('/signup', methods=['POST'])
def signup_post():
    """username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(usr=username).first()

    if user:
        flash('Username already exists')
        return redirect(url_for('auth.signup'))

    new_user = User(usr=username, pub=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()
    """
    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))