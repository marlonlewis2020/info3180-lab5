# Add any form classes for Flask-WTF here
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed, FileSize
from wtforms import StringField, TextAreaField
from wtforms.validators import InputRequired, DataRequired

class MovieForm (FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    poster = FileField('Poster', validators=[FileRequired(), FileSize(max_size=4000000), FileAllowed(["jpg", "png"], message="Image Files Only!")])