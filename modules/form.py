from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField

class LoginForm(FlaskForm):
    id_number = StringField(label="ID Number", validators=[validators.DataRequired(message="Provide a ID Number for Login."), validators.length(min=9,max=9,message="Length not valid. (length=9)"), validators.Regexp(regex="\\d{4}-\\d{4}",message="Format not valid.")])
    password = PasswordField(label="Password", validators=[validators.DataRequired(message="Provide a Password.")])