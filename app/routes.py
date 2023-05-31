from .import app
from flask import render_template, send_from_directory, request
from .models import Marvel, User
import json, os

apikey = os.environ.get('API_KEY')
pvapikey = os.environ.get('PV_API_KEY')
hash = os.environ.get('HASH_PRE')+pvapikey+apikey

@app.route('/')
def login():
    return render_template('login.html', methods=['GET', 'POST'])


@app.route('/defaulthome', methods = ['GET'])
def defaulthome():
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


@app.route('/home', methods=['GET', 'POST'])
def homepage():
    context = {
        'posts': Marvel.query.get('name')
    }
    return render_template('homepage.html', **context)


@app.route('/singlechar', methods=['GET','POST'])
def blog_single():
    if request.method == 'GET':
        query = request.form['query'] 
        character_url = f'https://gateway.marvel.com:443/v1/public/characters={query}&ts=123&apikey={apikey}&hash={(hashlib.md5(hash.encode())).hexdigest()}'
    return render_template('blog/single.html', query=query)


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


@app.route('/passchange', methods=['GET', 'POST'])
def change_password():
    return render_template('passchange.html')
