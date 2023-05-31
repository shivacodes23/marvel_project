from datetime import datetime
from app import db

# from flask_login import UserMixin
# from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    token = db.Column(db.String)
    character = db.Relationship('Marvel', backref='user', lazy='dynamic')
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User: {self.email}>'

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     self.generate_password(self.password)

    # def check_password(self, password_to_check):
    #     return check_password_hash(self.password, password_to_check)

    # def generate_password(self, password_create_salt_from):
    #     self.password = generate_password_hash(password_create_salt_from)

    # def to_dict(self):
    #     data = {
    #         'id': self.id,
    #         'first_name': self.first_name,
    #         'last_name': self.last_name,
    #         'email': self.email
    #     }
    #     return data


class Marvel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.Text, nullable=True)
    comic_appearances = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # def __repr__(self):
    #     return '<Marvel: {self.name}...>'

    # def to_dict(self):
    #     data = {
    #         'id': self.id,
    #         'description': self.description,
    #         'date_created': self.date_created,
    #         'comic_apps': self.comic_appearances,
    #         'owner': self.owner_id,
    #         'date_created': self.date_created
    #     }
    #     return data
