from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, RadioField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired, EqualTo

# Create Login Form
class LoginForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired()])
	password = PasswordField("Password", validators=[DataRequired()])
	submit = SubmitField("Submit")
	
# Create a User Form
class UserForm(FlaskForm):
	firstname = StringField("First Name", validators=[DataRequired()])
	lastname = StringField("Last Name", validators=[DataRequired()])
	username = StringField("Username", validators=[DataRequired()])
	email = StringField("Email", validators=[DataRequired()])
	gender = RadioField('Gender', choices=[('Male'),('Female')])
	password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Passwords Must Match!')])
	password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
	submit = SubmitField("Submit")


# Create a VoteEvent Form
class VoteEventForm(FlaskForm):
	name = StringField("Event Name", validators=[DataRequired()])
	description = TextAreaField("Event Description")
	participant1 = StringField("Candidate 1", validators=[DataRequired()])
	participant2 = StringField("Candidate 2", validators=[DataRequired()])
	participant3 = StringField("Candidate 3")
	participant4 = StringField("Candidate 4")
	participant5 = StringField("Candidate 5")
	participant6 = StringField("Candidate 6")
	participant7 = StringField("Candidate 7")
	participant8 = StringField("Candidate 8")
	participant9 = StringField("Candidate 9")
	participant10 = StringField("Candidate 10")
	submit = SubmitField("Submit")

# Create a CloseEvent Form
class CloseEventForm(FlaskForm):
	selectedevents = SelectMultipleField('Select Events to close')
	submit = SubmitField("Submit")

# Create a CastVote Form
class CastVoteForm(FlaskForm):
	selectedparticipant = RadioField('Select Candidate to Vote!')
	submit = SubmitField("Submit")