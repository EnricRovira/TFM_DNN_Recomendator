from wtforms import (Form, TextField, validators, SubmitField, DecimalField, IntegerField)

class ReusableForm(Form):
    """User entry form for entering specifics for generation"""

    # Starting customer
    customer = IntegerField('Enter the top customer to be recommended:', default=5,
                             validators=[validators.InputRequired(),
                                         validators.NumberRange(min=1, max=20,
                                         message='Must be between 1 and 20')])
    # top predictions
    top = IntegerField('Top recommendations:', default=0,
                             validators=[validators.InputRequired(),
                                         validators.NumberRange(min=1, max=1000,
                                         message='Must be between 1 and 1000')])
    # Submit button
    submit = SubmitField("Enter")