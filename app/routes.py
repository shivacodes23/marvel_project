from .import app
from flask import render_template, send_from_directory, request, redirect, flash, url_for, get_flashed_messages
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
import random

apikey = os.environ.get('API_KEY')
pvapikey = os.environ.get('PV_API_KEY')
hashpre = os.environ.get('HASH_PRE')
hash = hashpre+pvapikey+apikey

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
            "comics": char.get('comics', ""),
            "thumbnail": char.get('thumbnail', "")
        }
        char_list.append(char_template)
    char_list = {'chars': char_list}
    return render_template('defaulthome.html', **char_list)


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
    return render_template('defaulthome.html', **context)


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


@app.route('/save', methods=['GET','POST'])
def savelist():
    context = {'character': ""}
    if request.method == 'POST':
        user_choice = request.form.get('query').lower()
        character_data = requests.get(
            f"http://gateway.marvel.com/v1/public/characters?name={user_choice}&ts=123&apikey=fa8ab8be073cf4796a0884496945a04f&hash={(hashlib.md5(hash.encode())).hexdigest()}")
        context['character'] = character_data.json()
        comics = context['character']['data']['results'][0]['comics']['items']
        comics_list = []
        for comic in comics:
            comics_list.append(comic['name'])
            context['comic_list'] = comics_list
        print(context)    
        name = request.form.get('name')
        character_id = request.form.get('character_id')
        description = request.form.get('description')
        comics_appeared_in = request.form.get('comic_appearances')
        super_power = request.form.get('super_power')
        image = request.form.get('image')
        character = Character(name=name,character_id=character_id,description=description,comics_appeared_in=comics_appeared_in,super_power=super_power,image=image)
        db.session.add(character)
        db.session.commit()
        user_list = user_list.append(context)
        return render_template('userlist.html',**context)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        f_name = request.form.get('firstname')
        l_name = request.form.get('lastname')
        print(f"FULL NAME: {f_name + ' ' + l_name}")
        user = User(email=email, password=password,
                    first_name=f_name, last_name=l_name)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering', 'success')
        login_user(user)
        return redirect(url_for('homepage'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # accept user data and check if user exists and password is correct.
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email.lower()).first()
        print(f"USER INFO:{user.first_name, user.last_name}")
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('homepage'))
        else:
            flash(
                'Either that was an invalid password or username. Try again. ', 'danger')
            return redirect(request.referrer)
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    flash('User logged out successfully', 'danger')
    return redirect(url_for('homepage'))

