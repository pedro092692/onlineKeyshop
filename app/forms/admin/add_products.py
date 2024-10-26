from app.forms.extensions import *

class AddProduct(FlaskForm):
    product_name = StringField(label='Product Name', validators=[DataRequired()],
                               render_kw={'placeholder': 'Product Name'})
    product_category = SelectField(label='Product Category', coerce=int, validators=[DataRequired()])
    product_subcategory = SelectField(label='Product Subcategory', coerce=int, validators=[DataRequired()])
    product_platform = SelectField(label='Product Platform', coerce=int, validators=[DataRequired()])
    product_key_code = StringField(label='Product Key Code', validators=[DataRequired()])
    product_price =  DecimalField(label='Product Price', validators=[DataRequired()],
                               render_kw={'placeholder': 'Product Price'})
    submit = SubmitField(label='Add Product')