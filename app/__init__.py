from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment

app = Flask(__name__)
app.config.from_object(Config)

#ORM - Object Relational Mapper
db = SQLAlchemy(app)
migrate = Migrate(app, db)
moment = Moment(app)

from .import routes, models 
# db.init_app(app)
# migrate.init_app(app, db)
# moment.init_app(app)
# login_manager.init_app(app)