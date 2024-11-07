from flask_wtf import FlaskForm
from wtforms import StringField, validators, IntegerField, SelectField


class VerificationForm(FlaskForm):
    contribution_name = StringField(label="Name", validators=[validators.DataRequired(message="Provide a Name for Identification."), validators.length(min=1,max=50,message="Length not valid. (min=1, max=50)")])
    block_rep = StringField(label="Block Rep", validators=[validators.DataRequired(message="Provide a Name for Identification."), validators.length(min=1,max=50,message="Length not valid. (min=1, max=50)")])
    year_level = SelectField(label="Year Level", choices=[('1', "1st year"), ('2', "2nd year"), ('3', "3rd year"), ('4', "4th year")])
    program_code = SelectField(label="Program Code", choices=[])
    total_amount = IntegerField(label="Total Amount (in Php)", validators=[validators.DataRequired(message="Provide the total."), validators.NumberRange(message="Amount not less than 0.", min=0)])