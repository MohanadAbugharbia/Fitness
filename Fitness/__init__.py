from flask import (
    Flask,
    render_template
)
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

from tools import (
    DatabaseConfig,
    ApplicationConfig
)


app = Flask(__name__)

db: SQLAlchemy = SQLAlchemy()

login_manager = LoginManager()


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


def create_app(database_config: DatabaseConfig, application_config: ApplicationConfig):
    app.config['SQLALCHEMY_DATABASE_URI'] = f'{database_config.engine}://{database_config.user}:{database_config.password}@{database_config.host}:{database_config.port}/{database_config.database}'

    app.secret_key = application_config.secret_key
    login_manager.login_view = 'auth.login'

    db.init_app(app)
    login_manager.init_app(app)
    
    from Fitness.auth.views import auth
    from Fitness.profile.views import profile
    app.register_blueprint(auth)
    app.register_blueprint(profile)

    ctx = app.test_request_context()
    ctx.push()

    db.create_all()

    return app