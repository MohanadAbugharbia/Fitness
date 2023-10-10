from flask_wtf import Form
from wtforms import StringField,PasswordField, BooleanField
from wtforms import validators
from flask_login import UserMixin
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)


from Fitness import db, app


class User(UserMixin, db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    
    @property
    def password(self):
        raise AttributeError("Password is readonly")

    @password.setter
    def password(self,new_password):
       self.password_hash = generate_password_hash(new_password,method='pbkdf2:sha512',salt_length=64)

    def verify_password(self,password):
       return check_password_hash(self.password_hash, password)


    def __str__(self) -> str:
        return f"User: {self.id},{self.email}"

class LoginForm(Form):
    email = StringField('Email',[validators.DataRequired()])
    password = PasswordField('Password',[validators.DataRequired()])
    remember_me = BooleanField('Remember Me')


class SignupForm(Form):
    firstname = StringField('First Name', [validators.DataRequired()])
    lastname = StringField('Last Name', [validators.DataRequired()])
    email = StringField('Email', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])