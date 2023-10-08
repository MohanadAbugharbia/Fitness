from flask import (
    Flask,
    render_template
)
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

app = Flask(__name__)

DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_HOST = os.environ['DB_HOST']
DB_PORT = os.environ['DB_PORT']
DB_NAME = os.environ['DB_NAME']
DB_ENGINE = os.environ['DB_ENGINE']

SECRET_KEY = os.environ['SECRET_KEY']


app.config['SQLALCHEMY_DATABASE_URI'] = f'{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

db: SQLAlchemy = SQLAlchemy(app)

app.secret_key = SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

ctx = app.test_request_context()
ctx.push()


from Fitness.auth.views import auth
app.register_blueprint(auth)

from Fitness.profile import profile
app.register_blueprint(profile)

db.create_all()

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')
