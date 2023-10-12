from datetime import datetime
from flask_wtf import Form
from wtforms import DateField, FloatField
from wtforms import validators
import sqlalchemy as sa

from Fitness import db, app


class Weight(db.Model):
    __tablename__ = "weights"

    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), primary_key=True)
    date = sa.Column(sa.DateTime, nullable=False, primary_key=True)
    weight = sa.Column(sa.Float, nullable=False)

class WeightForm(Form):
    date = DateField("Date", [validators.DataRequired()], default=datetime.today)
    weight = FloatField("Weight", [validators.DataRequired()])

