# No modifications necessary to account for SQL

from flask_wtf import FlaskForm
from wtforms import StringField, TextField, BooleanField
from wtforms.validators import DataRequired


class TodoForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    description = TextField('description', validators=[DataRequired()])
    done = BooleanField('done', validators=[])
