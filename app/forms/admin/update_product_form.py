from app.forms.extensions import *

class UpdateProduct(FlaskForm):
    name = StringField(label='Product Name', validators=[DataRequired()])
    product_category = SelectField(label='Product Category', coerce=int, validators=[DataRequired()])
    product_subcategory = SelectField(label='Product Subcategory', coerce=int, validators=[DataRequired()])
    product_platform = SelectField(label='Product Platform', coerce=int, validators=[DataRequired()])
    submit = SubmitField(label='Update Product')