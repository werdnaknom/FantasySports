from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,
SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from app.models import Products


class CreateProductForm(FlaskForm):
    name = StringField('New Product Name:', validators = [DataRequired()])
    submit = SubmitField('Submit')
