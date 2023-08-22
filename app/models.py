from datetime import datetime
from app import db, login_manager
import random
import string
from flask_login import UserMixin
# import typing
import bcrypt


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    token = db.Column(db.String(255), default=''.join(
        random.choice(string.ascii_letters) for i in range(25)))
    character = db.Relationship('Character', backref='user', lazy='dynamic')
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User: {self.email}>'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(self.password.encode('utf-8'), salt)
        self.password = hashed_password.decode('utf-8')

    def check_password(self, password) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def to_dict(self):
        data = {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        }
        return data


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    description = db.Column(db.Text, nullable=True)
    super_power = db.Column(db.Text, nullable=True)
    comic_appearances = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    character_id = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Character: {self.name}, Owner: {self.user_id}>'

    def to_dict(self):
        from app.models import User
        data = {
            'id': self.id,
            'name': self.name,
            'character_id': self.character_id,
            'description': self.description,
            'comics_appeared_in': self.comic_appearances,
            'super_power': self.super_power,
            'date_created': self.date_created,
            'image': self.image,
            'user_id': User.query.get(self.user_id).to_dict()
        }
        return data
