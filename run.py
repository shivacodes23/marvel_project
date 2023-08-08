from app import database
from datetime import datetime
import requests
import hashlib
# from flask import Flask
# from flask import render_template
# import json
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask_moment import Moment
# from config import Config
# from flask_login import LoginManager, UserMixin
import os
from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash
from app import routes, models
from app import app

# login_manager = LoginManager()

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(user_id)
# user_choice = input(
#     'Enter the Marvel Superhero you would like to view information for.').lower()

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

apikey = os.environ.get('API_KEY')
pvapikey = os.environ.get('PV_API_KEY')
hash = os.environ.get('HASH_PRE')+pvapikey+apikey

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



# for name in marvel_chars:
#     if name['name'] == 'Thor':
#         print(name['name'])

# for name in marvel_chars:
#     if name['name'] == 'Thor':
#         print(name['description'])

# for name in marvel_chars:
#     if name['name'] == 'Thor':
#         print(name['id'])


# for name in marvel_chars:
#     if name['name'] == 'Thor':
#         print(name['comics'])

# for name in marvel_chars:
#     if name['name'] == 'Thor':
#         print(name['thumbnail'])

# marvel_dict = {'chars': marvel_chars}


# with open('marvel_chars.txt', 'w') as f:
#     json.dump(marvel_dict, f)


# comics = data['data']['results'][0]['comics']['items']
# comics_list = []
# for comic in comics:
#     comics_list.append(comic['name'])
# # print(f'List of all comics: {comics}')
# print(f'Comic names: {comics_list}')
# print(data['data']['results'][0]['id'])
# print(data['data']['results'][0]['name'])
# print(f"DESCRIPTION: {data['data']['results'][0]['description']}")


# def register(app):
#     @app.cli.group()
#     def blueprint():
#         """Blueprint creation commands."""
#         pass

#     @blueprint.command()
#     @click.argument('name')
#     def create(name):
#         """Create new Flask blueprint"""

#         basedir = os.path.abspath(os.path.dirname(
#             __name__)) + f'/app/blueprints/{name}'

#         try:
#             # check if the blueprint directory already exists.
#             if not os.path.exists(basedir):
#                 os.makedirs(basedir)
#                 filenames = ['__init__', 'routes', 'models']
#                 [open(f'{basedir}/{file}.py', 'w') for file in filenames]
#                 print("Blueprint created successfully.")
#         except Exception as error:
#             print(
#                 f'Something went wrong with creating your blueprint called {name}.')
#             print(error)

if (__name__) == '__main__':
    app.run(debug=True)
