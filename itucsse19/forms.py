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
    password = PasswordField("Password" , validators = [DataRequired() , Length(min = 9)])
    confirmPass = PasswordField("Confirm Password" , validators = [DataRequired() , EqualTo("password")])
    institution = StringField('Institution', validators=  [DataRequired()])
    user_type = SelectField('Select User Type', choices=[('High School Student', 'High School Student'),
                                                         ('University Student', 'University Student'),
                                                         ('University Representative', 'University Representative'),
                                                         ('High School Representative', 'High School Representative')])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = StringField("Email" , validators= [DataRequired() , Email()])
    password = PasswordField("Password" , validators = [DataRequired()])
    submit = SubmitField("Log In")

class UpdateInsInfoForm(FlaskForm):
    webaddress = StringField("Webaddress", validators=[DataRequired()])
    info = StringField("Information",validators=[DataRequired()] )
    contactInfo = StringField('Contact Info' ,validators=[DataRequired()] )
    submit = SubmitField("Update")

