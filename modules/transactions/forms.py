from flask_wtf import FlaskForm
from wtforms import StringField, validators, IntegerField, SelectField, TextAreaField

class PaymentForm(FlaskForm):
    item_name = StringField(label="Item Name", validators=[validators.DataRequired(message="Provide a Name for Identification."), validators.length(min=1,max=50,message="Length not valid. (min=1, max=50)")])
    academic_year = StringField(label="Academic Year", validators=[validators.DataRequired(message="Provide the academic year."), validators.length(min=9,max=9,message="Length not valid. (length=9)"), validators.Regexp(regex="\\d{4}-\\d{4}",message="Format not valid.")])
    payer_id = StringField(label="ID Number", validators=[validators.DataRequired(message="Provide an ID e.g. 2021-1756"), validators.length(min=9,max=9,message="Length not valid. (length=9)"), validators.Regexp(regex="\\d{4}-\\d{4}",message="Format not valid.")])
    payment_mode = SelectField(label="Payment Mode", choices=[('Cash', "Cash"), ('GCash', "GCash"), ('Others', "Others")])
    amount = IntegerField(label="Amount", validators=[validators.DataRequired(message="Provide an amount.")])