# from app import db
# from datetime import datetime

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(50))
#     last_name = db.Column(db.String(50))
#     email = db.Column(db.String(100), unique=True)
#     password = db.Column(db.String(255))
#     token = db.Column(db.String)
#     character = db.Relationship('Marvel', backref='user', lazy='dynamic')
#     date_created = db.Column(db.DateTime, default=datetime.utcnow)
