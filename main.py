from . import db, login_manager
from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from .models import *
main = Blueprint('main', __name__)

@main.route('/vault')
def handle_needs_login():
    print(User.Logins)
    #current_user.Logins += "google.com, anthony, password"
    L = "google.com, anthony, password|facebook.com, bob, qoojadkm|"
    logins = L.split("|")
    l = []
    for i in range(0, len(logins)):
        if(logins[i] == ''):
            logins.remove(logins[i])
        else:
            l.append(logins[i].split(","))
    return render_template('vault.html', log = l )

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.usr)
