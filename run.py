from datetime import datetime
import requests
import hashlib
from flask import Flask
from flask import render_template
import json
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from .config import Config
from flask_login import LoginManager, UserMixin
import os, click
from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)


login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()
moment = Moment()


config_class = Config
app = Flask(__name__)
app.config.from_object(config_class)
db.init_app(app)
migrate.init_app(app,db)
moment.init_app(app)
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/')
def login():
    return render_template('login.html', methods=['POST'])

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route('/passchange', methods=['GET', 'POST'])
def change_password():
    return render_template('passchange.html')
# user_choice = input(
#     'Enter the Marvel Superhero you would like to view information for.').lower()

apikey = os.environ.get('API_KEY')
pvapikey = os.environ.get('PV_API_KEY')
hash = os.environ.get('HASH_PRE')+pvapikey+apikey
# api_link = f"http://gateway.marvel.com/v1/public/characters?name={user_choice}&ts=123&apikey={apikey}&hash={(hashlib.md5(hash.encode())).hexdigest()}"
# print(f"API_KEY: {apikey}")
# print(f"PRIVATE_KEY: {pvapikey}")
# print(f"HASH: {hash}")
# print(f"API_LINK: {api_link}")

# response = requests.get(api_link)
# data = response.json()
# print(data)
# characters_url = f'https://gateway.marvel.com:443/v1/public/characters?limit=100&ts=123&apikey={apikey}&hash={(hashlib.md5(hash.encode())).hexdigest()}'
# all_characters = requests.get(characters_url).json()['data']['results']  # list of dict
# print(all_characters)

# complete_list = (all_characters['data']['results'])
# print(all_characters['data']['count'])

marvel_chars = []
offset = 0

while len(marvel_chars) < 1562:
    characters_url = f'https://gateway.marvel.com:443/v1/public/characters?limit=100&offset={offset}&ts=123&apikey={apikey}&hash={(hashlib.md5(hash.encode())).hexdigest()}'
    all_characters = requests.get(characters_url).json()['data']['results']  # list of dict

    for i in range(len(all_characters)):
        cur_char = all_characters[i]  # dict
        char_template = {
            "id": cur_char['id'],
            "name": cur_char['name'],
            "description": cur_char['description'],
            "comics": [],
            "thumbnail": str(cur_char['thumbnail']['path'] + "." + cur_char['thumbnail']['extension'])
        }

        for comic in cur_char['comics']['items']:  # list of dict
            char_template['comics'].append(comic['name'])

        marvel_chars.append(char_template)

    offset += 100

print(f'>>>> LENGTH OF MARVEL CHARS LIST: {len(marvel_chars)}')

marvel_dict = {'chars': marvel_chars}

with open('marvel_chars.txt', 'w') as f:
    json.dump(marvel_dict, f)

# comics = data['data']['results'][0]['comics']['items']
# comics_list = []
# for comic in comics:
#     comics_list.append(comic['name'])
# # print(f'List of all comics: {comics}')
# print(f'Comic names: {comics_list}')
# print(data['data']['results'][0]['id'])
# print(data['data']['results'][0]['name'])
# print(f"DESCRIPTION: {data['data']['results'][0]['description']}")


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.Text)
    comic_appearances = db.Column(db.Integer)
    superpower = db.Column(db.String)
    owner = db.Column(db.String, db.ForeignKey('user_id'))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.generate_password(self.password)

    def check_password(self, password_to_check):
        return check_password_hash(self.password, password_to_check)

    def generate_password(self, password_create_salt_from):
        self.password = generate_password_hash(password_create_salt_from)

    def to_dict(self):
        data = {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        }
        return data
    
    def __repr__(self):
        return f'<User: {self.email}>'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_dict(self):
        data = {
            'id': self.id,
            'body': self.body,
            'date_created': self.date_created,
            'user_id': User.query.get(self.user_id).to_dict()
        }
        return data

    def __repr__(self):
        return '<Post: {self.body[:10]}...>'


def register(app):
    @app.cli.group()
    def blueprint():
        """Blueprint creation commands."""
        pass

    @blueprint.command()
    @click.argument('name')
    def create(name):
        """Create new Flask blueprint"""

        basedir = os.path.abspath(os.path.dirname(
            __name__)) + f'/app/blueprints/{name}'

        try:
            # check if the blueprint directory already exists.
            if not os.path.exists(basedir):
                os.makedirs(basedir)
                filenames = ['__init__', 'routes', 'models']
                [open(f'{basedir}/{file}.py', 'w') for file in filenames]
                print("Blueprint created successfully.")
        except Exception as error:
            print(
                f'Something went wrong with creating your blueprint called {name}.')
            print(error)



if (__name__) == 'run':
    app.run()
