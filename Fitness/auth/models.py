from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, EmailField
from wtforms import validators
from flask_login import UserMixin
import sqlalchemy as sa
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)


from Fitness import db, app


class User(UserMixin, db.Model):
    __tablename__ = "users"
    
    id = sa.Column(sa.Integer, primary_key = True)
    email = sa.Column(sa.String(100), unique=True, nullable=False)
    firstname = sa.Column(sa.String(100), nullable=False)
    lastname = sa.Column(sa.String(100), nullable=False)
    password_hash = sa.Column(sa.String(256), nullable=False)
    last_login = sa.Column(sa.DateTime, nullable=True)
    
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
    email = EmailField('Email',[
        validators.DataRequired(),
        validators.InputRequired(),
        validators.Email(message="Invalid Email"),
    ])
    password = PasswordField('Password',[
        validators.DataRequired(),
        validators.InputRequired(),
        validators.Length(min=8, message="Password must be at least 8 characters"),
        validators.Length(max=64, message="Password must be less than 64 characters"),
    ])
    remember_me = BooleanField('Remember Me')


class SignupForm(Form):
    firstname = StringField('First Name', [
        validators.DataRequired("First Name is required."),
        validators.InputRequired(),
    ])
    lastname = StringField('Last Name', [
        validators.DataRequired("Last Name is required."),
        validators.InputRequired(),
    ])
    email = EmailField('Email',[
        validators.DataRequired("Email is required."),
        validators.InputRequired(),
        validators.Email(message="Invalid Email"),
    ])
    password = PasswordField('Password',[
        validators.DataRequired("Password is required."),
        validators.InputRequired(),
        validators.Length(min=8, message="Password must be at least 8 characters"),
        validators.Length(max=64, message="Password must be less than 64 characters"),
    ])