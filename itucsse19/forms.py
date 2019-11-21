from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, IntegerField, TextField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo
import datetime
from datetime import date

class RegistrationForm(FlaskForm):
    #Validators are used to give conditions for the username , password etc.
    name = StringField("Name" , validators=  [DataRequired()])
    surname = StringField("Surname" , validators= [DataRequired()])
    username = StringField("Username" , validators = [DataRequired() , Length( min = 5 , max = 15)])
    email = StringField("Email" , validators= [DataRequired() , Email()])
    password = PasswordField("Password" , validators = [DataRequired() , Length(min = 5 , max = 15)])
    confirmPass = PasswordField("Confirm Password" , validators = [DataRequired() , EqualTo("password")])
    institution = StringField('Institution', validators=  [DataRequired()])
    user_type = SelectField('Select User Type' , choices=[('High School Student' , 'High School Student') , ('University Student' , 'University Student')])
    submit = SubmitField("Register")