# Add any form classes for Flask-WTF here
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed, FileSize
from wtforms import StringField, TextAreaField
from wtforms.validators import InputRequired, DataRequired, Length

class MovieForm (FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(min=2, max=80)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=2, max=80)])
    poster = FileField('Poster', validators=[FileRequired(), FileSize(max_size=4000000), FileAllowed(["jpg", "png"], message="Image Files Only!")])