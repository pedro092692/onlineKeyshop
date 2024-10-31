from cProfile import label
from wtforms.fields.simple import HiddenField

from app.forms.extensions import *

class PaymentForm(FlaskForm):
    amount = HiddenField(label='Amount', validators=[DataRequired()])
    product_id = HiddenField()
    submit = SubmitField(label='Pay With Paypal')