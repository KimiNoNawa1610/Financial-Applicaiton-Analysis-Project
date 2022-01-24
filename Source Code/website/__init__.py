from venv import create
from flask import Flask
from os import path
from flask_login import LoginManager

#create a database
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = "database.db"

#initialize the website basic config from the flask package
def create_app():

    app = Flask(__name__)

    app.config['SECRET_KEY'] = '2022BrokeAF***COVID' #seret key to protect cache and private data of the website

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # The sqlite database is store at this location

    db.init_app(app)

    from .views import views # assign the homepage to the contructor

    from .auth import auth #assign auth page to the constructor

    app.register_blueprint(views, url_prefix='/')

    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Stock

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app): #check whether the dabase exist. If not, create one
    if not path.exists('website/' + DB_NAME):
        db.create_all(app = app)
        print("Created Database!!!!")



