from app.forms.extensions import *

class AddKey(FlaskForm):
    key_value = StringField(label='Key Value', validators=[DataRequired()])
    price = DecimalField(label='Key Price', validators=[DataRequired()])
    submit = SubmitField(label='Add Key')