from app.forms.extensions import *

class AddCategory(FlaskForm):
    name = StringField(label='Category Name', validators=[DataRequired()])
    submit = SubmitField(label='Add Category')