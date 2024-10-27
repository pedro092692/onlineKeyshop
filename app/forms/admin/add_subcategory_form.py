from app.forms.extensions import *

class SubcategoryForm(FlaskForm):
    name = StringField(label='Subcategory Name', validators=[DataRequired()])
    category_id = SelectField(label='Category', coerce=int, validators=[DataRequired()])
    submit = SubmitField(label='Add Subcategory')