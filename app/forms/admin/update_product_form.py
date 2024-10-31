from app.forms.extensions import *

class UpdateProduct(FlaskForm):
    name = StringField(label='Product Name', validators=[DataRequired()])
    product_category = SelectField(label='Product Category', coerce=int, validators=[DataRequired()])
    product_subcategory = SelectField(label='Product Subcategory', coerce=int, validators=[DataRequired()])
    product_platform = SelectField(label='Product Platform', coerce=int, validators=[DataRequired()])
    image_url = StringField(label='Image Url', validators=[DataRequired(), URL()],
                            render_kw={'placeholder': 'Image URL'})
    submit = SubmitField(label='Update Product')