from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

#Search form
class SearchForm(FlaskForm):
    search = StringField("search", validators=[DataRequired()])
    submit = SubmitField("Submit")

