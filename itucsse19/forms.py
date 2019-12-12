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

class AddAddress(FlaskForm):
    city = StringField("City", validators=[DataRequired()])
    address = StringField("Address",validators=[DataRequired()] )
    submit = SubmitField("Add")

class CreateEvent(FlaskForm):
    time = datetime.datetime.now()
    hour = time.hour
    minute = time.minute
    mytime = str(hour) + '.' + str(minute)
    event_name = StringField("Event Name", validators=[DataRequired()])
    date = StringField("Date of Event", default=date.today(), validators=[DataRequired()])
    time = StringField('Event Time', default=mytime, validators=[DataRequired()])
    duration = StringField('Duration', default="02.00 hours", validators=[DataRequired()])
    address = RadioField('Address',  validators=[DataRequired()])
    venue = StringField('Venue', validators=[DataRequired()])
    info = StringField("Explanation", validators=[DataRequired()])
    quota = IntegerField("Maximum Number of Participants", validators=[DataRequired()])
    isOpen = RadioField('Do you want students to participate event without invitation?',
                           choices=[(True, 'Y'), (False, 'N')], validators=[DataRequired()])


    submit = SubmitField("Create")

