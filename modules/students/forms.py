from flask_wtf import FlaskForm
from wtforms import StringField, validators, SelectField

class StudentForm(FlaskForm):
    full_name = StringField(label="Name", validators=[validators.DataRequired(message="Provide a Name for Identification."), validators.length(min=1,max=155,message="Length not valid. (min=1, max=155)")])
    id_number = StringField(label="ID Number", validators=[validators.DataRequired(message="Provide an academic year e.g. 2021-1756"), validators.length(min=9,max=9,message="Length not valid. (length=9)"), validators.Regexp(regex="\\d{4}-\\d{4}",message="Format not valid.")])
    gender = SelectField(label="Gender", choices=[('F', "Female"), ('M', "Male")])
    year_level = SelectField(label="Year Level", choices=[('1', "1st year"), ('2', "2nd year"), ('3', "3rd year"), ('4', "4th year")])
    program_code = SelectField(label="Program Code", choices=[])
    note = StringField(label="Note", validators=[validators.length(min=1,max=255,message="Length not valid. (min=1, max=255)")])