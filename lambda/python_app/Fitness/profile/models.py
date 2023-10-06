from flask_wtf import Form
from wtforms import DateField, FloatField
from wtforms import validators
from flask_login import UserMixin

from Fitness import db, app
from datetime import datetime


class Weight(db.Model):
    __tablename__ = "weights"

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    date = db.Column(db.DateTime, nullable=False, primary_key=True)
    weight = db.Column(db.Float, nullable=False)

class WeightForm(Form):
    date = DateField("Date", [validators.DataRequired()], default=datetime.today)
    weight = FloatField("Weight", [validators.DataRequired()])

