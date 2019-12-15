from . import db, login_manager
from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from .models import *
import ast

main = Blueprint('main', __name__)
L = "google.com, anthony, password|facebook.com, bob, qoojadkm|"
@main.route('/vault')
@login_required
def handle_needs_login():
    global L
    print(L, flush=True)
    print(User.Logins)
    #current_user.Logins += "google.com, anthony, password"

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
@main.route('/new', methods=['POST'])
def new():
    global L
    saveName = request.form.get('saveName')
    savePassword = request.form.get('savePassword')
    saveWebsite = request.form.get('saveWebsite')


    L +=  saveWebsite + ", " + savePassword + ", " + saveName + "|"
    return handle_needs_login()

@main.route('/delete', methods=['POST'])
def delete():
    global L
    toDelete = request.form.get('delete')
    toDelete = ast.literal_eval(toDelete)
    L = L.strip(toDelete[0] + ", " + toDelete[1] + ", " + toDelete[2] + "|")
    print(L, flush=True)
    return handle_needs_login()