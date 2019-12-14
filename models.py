from . import db, login_manager
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    usr = db.Column(db.String(100), unique=True) # username
    pub = db.Column(db.String(100))              # public key

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))