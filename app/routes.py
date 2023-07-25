from .import app
from flask import render_template, send_from_directory, request, redirect, flash, url_for,get_flashed_messages
from .models import Character, User
import json
from app import db
import os
import requests
import hashlib
from flask import jsonify
from flask_login import current_user, login_user, logout_user
from wtforms import Form, BooleanField, StringField, PasswordField, validators, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
import bcrypt

apikey = os.environ.get('API_KEY')
pvapikey = os.environ.get('PV_API_KEY')
hashpre = os.environ.get('HASH_PRE')
hash = hashpre+pvapikey+apikey


class RegistrationForm(Form):
    first_name = StringField('first_name', [validators.Length(min=4, max=25)])
    last_name = StringField('last_name', [validators.Length(min=4, max=25)])
    username = StringField('Username', [validators.Length(min=4, max=40)])
    # email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Register')


class LoginForm(Form):
    username = StringField('Username', [validators.Length(
        min=4, max=25)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=30)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')


with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def search():
    print("***HITS SEARCH ACTION***")
    context = {'character': ""}
    if request.method == 'POST':
        try:
            user_choice = request.form.get('query').lower()
            print(f'USER CHOICE: {user_choice}')
            # print("BEFORE MAKING API CALL")
            character_data = requests.get(
                f"http://gateway.marvel.com/v1/public/characters?name={user_choice}&ts=123&apikey=fa8ab8be073cf4796a0884496945a04f&hash={(hashlib.md5(hash.encode())).hexdigest()}")
            # print("AFTER MAKING API CALL")
            # print(character_data.json())
            context['character'] = character_data.json()
            print(f"CONTEXT DATA: {context['character']}")
            # char_data = character_data.get('results')[0]
        except:
            print(
                "Either the character cannot be found or worse...you're looking for a DC character :(", 'danger')
            return redirect(request.referrer)
        print(f"CONTEXT: {context}")
        comics = context['character']['data']['results'][0]['comics']['items']
        print(comics)
        comics_list = []
        for comic in comics:
            comics_list.append(comic['name'])
            context['comic_list'] = comics_list
        print(comics_list)
        return render_template('single.html', **context)
    return render_template('defaulthome.html', **context)


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/gallery', methods=['GET', 'POST'])
def homepage():
    context = {'character': ""}
    if request.method == 'POST':
        try:
            user_choice = request.form.get('query').lower()
            print(f'USER CHOICE: {user_choice}')
            # print("BEFORE MAKING API CALL")
            character_data = requests.get(
                f"http://gateway.marvel.com/v1/public/characters?name={user_choice}&ts=123&apikey=fa8ab8be073cf4796a0884496945a04f&hash={(hashlib.md5(hash.encode())).hexdigest()}")
            # print("AFTER MAKING API CALL")
            # print(character_data.json())
            context['character'] = character_data.json()
            print(f"CONTEXT DATA: {context['character']}")
            # char_data = character_data.get('results')[0]
        except:
            print(
                "Either the character cannot be found or worse...you're looking for a DC character :(", 'danger')
            return redirect(request.referrer)
        print(f"CONTEXT: {context}")
        comics = context['character']['data']['results'][0]['comics']['items']
        print(comics)
        comics_list = []
        for comic in comics:
            comics_list.append(comic['name'])
            context['comic_list'] = comics_list
        print(comics_list)
        return render_template('single.html', **context)

    print(current_user.is_anonymous)
    file_path = app.static_folder + '/marvel_chars.txt'
    char_template = {}
    char_list = []
    with open(file_path, 'r') as file:
        data = file.read()
    for char in json.loads(data):
        char_template = {
            "id": char.get('id', ""),
            "name": char.get('name', ""),
            "description": char.get('description', ""),
            "comics": char.get('comics', []),
            "thumbnail": char.get('thumbnail', "")
        }
        char_list.append(char_template)
    context = {'chars': char_list}
    return render_template('homepage.html', **context)


@app.route('/singlechar', methods=['GET', 'POST'])
def blog_single():
    context = {'character': ""}
    if request.method == 'POST':
        try:
            user_choice = request.form.get('query').lower()
            print(f'USER CHOICE: {user_choice}')
            # print("BEFORE MAKING API CALL")
            character_data = requests.get(
                f"http://gateway.marvel.com/v1/public/characters?name={user_choice}&ts=123&apikey=fa8ab8be073cf4796a0884496945a04f&hash={(hashlib.md5(hash.encode())).hexdigest()}")
            # print("AFTER MAKING API CALL")
            # print(character_data.json())
            context['character'] = character_data.json()
            print(f"CONTEXT DATA: {context['character']}")
            # char_data = character_data.get('results')[0]
        except:
            print(
                "Either the character cannot be found or worse...you're looking for a DC character :(", 'danger')
            return redirect(request.referrer)
        print(f"CONTEXT: {context}")
        comics = context['character']['data']['results'][0]['comics']['items']
        print(comics)
        comics_list = []
        for comic in comics:
            comics_list.append(comic['name'])
            context['comic_list'] = comics_list
        print(comics_list)
    return render_template('single.html', **context)


@app.route('/register', methods=['GET', 'POST'])
def register():
    # form = RegistrationForm(request.form)
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        # data = request.form
        # user = User.query.filter_by(email=data.get('email')).first()
        # print("Hit's register option.")
        # username = form.username.data
        # print(f"NAME: {username}")
        # password = form.password.data
        # print(f"PASSWORD: {password}")
        # f_name = form.first_name.data
        # l_name = form.last_name.data
        # print(f'{f_name} {l_name}')
        # salt = bcrypt.generate_password_hash(password,24)
        # username = form.username.data
        # email = form.email.data
        # Hashing the password after encoding it.
        salt = bcrypt.gensalt()
        hashed_password_encoded = bcrypt.hashpw(password.encode('utf-8'), salt)
        hashed_password = hashed_password_encoded.decode('utf-8')
        print(f"HASHED PASSWORD: {hashed_password}")
        # user = User(name=form.username.data, password=hashed_password)
        user = User(email=email, password=hashed_password,username=username)
                    # first_name=f_name, last_name=l_name)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering', 'info')
        return render_template('login.html')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        # encode password
        password = form.password.data.encode('utf-8')
        # create a salt
        salt = bcrypt.gensalt()
        # create hash by combining password and salt.
        hashed_password_encoded = bcrypt.hashpw(password, salt)
        hashed_password = hashed_password_encoded.decode('utf-8')
        result = bcrypt.checkpw(password, hashed_password.encode('utf-8'))
        if result == True:
            login_user(User)
            return redirect(url_for('homepage'))
        else:
            flash(
                'Credentials do not match.Please check your username or password.Or User does not exist.')
            return redirect(request.referrer)
    return render_template('login.html', form=form)
