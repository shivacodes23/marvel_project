from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object(Config)

#ORM - Object Relational Mapper
db = SQLAlchemy(app)
migrate = Migrate(app, db)
moment = Moment(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from .import routes, models 

