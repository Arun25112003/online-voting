from flask import Flask, render_template, flash, redirect, url_for, session
from webforms import LoginForm, UserForm, VoteEventForm, CloseEventForm, CastVoteForm
from datetime import datetime 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash 
import secrets


# Create a Flask Instance
app = Flask(__name__)
DB_NAME = "database.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_NAME
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)

#DB migration metadata naming constraints
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db)

# Flask_Login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Create a route decorator
@app.route('/')
def index():
    return render_template("index.html")

# Create Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(username=form.username.data).first()
		if user:
			# Check the hash
			if check_password_hash(user.password_hash, form.password.data):
				login_user(user)
				session['id'] = user.id
				session['firstname'] = user.firstname
				return redirect(url_for('dashboard'))
			else:
				flash("Wrong Password - Try Again!")
		else:
			flash("That User Doesn't Exist! Try Again...")
	return render_template('login.html', form=form)

# Create Logout Page
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
	logout_user()
	session.pop('id', default=None)
	session.pop('firstname', default=None)
	flash("You Have Been Logged Successfully Out!")
	return redirect(url_for('login'))

@login_manager.user_loader
def load_user(user_id):
	return Users.query.get(int(user_id))

# Create SignUp Page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = UserForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(email=form.email.data).first()
		if user is None:
			# Hash the password!!!
			hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
			user = Users(username=form.username.data, firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data, gender=form.gender.data, password_hash=hashed_pw)
			db.session.add(user)
			db.session.commit()
			form.firstname.data = ''
			form.lastname.data = ''
			form.username.data = ''
			form.email.data = ''
			form.gender.data = ''
			form.password_hash.data = ''
			flash("User Added Successfully!")
			return redirect(url_for('login'))
		else:
			flash("An account already exists with the given email!")
	return render_template("signup.html", form=form)

# Create Dashboard Page
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
	voteevents = Voteevent.query.order_by(Voteevent.date_added)
	return render_template('dashboard.html',firstname=session['firstname'], voteevents=voteevents)

# Create createvoteevent Page
@app.route('/createvoteevent', methods=['GET', 'POST'])
@login_required
def createvoteevent():
	form = VoteEventForm()
	voteevent=None
	participants=None
	if form.validate_on_submit():
		voteevent = Voteevent(name=form.name.data, description=form.description.data, created_by=session['id'])
		db.session.add(voteevent)
		db.session.commit()
		voteevent = Voteevent.query.filter_by(name=form.name.data).first()
		participants = Participants(name=form.participant1.data, voteevent=voteevent.id)
		db.session.add(participants)
		db.session.commit()
		participants = Participants(name=form.participant2.data, voteevent=voteevent.id)
		db.session.add(participants)
		db.session.commit()
		if form.participant3.data:
			participants = Participants(name=form.participant3.data, voteevent=voteevent.id)
			db.session.add(participants)
			db.session.commit()
		if form.participant4.data:
			participants = Participants(name=form.participant4.data, voteevent=voteevent.id)
			db.session.add(participants)
			db.session.commit()
		if form.participant5.data:
			participants = Participants(name=form.participant5.data, voteevent=voteevent.id)
			db.session.add(participants)
			db.session.commit()
		if form.participant6.data:
			participants = Participants(name=form.participant6.data, voteevent=voteevent.id)
			db.session.add(participants)
			db.session.commit()
		if form.participant7.data:
			participants = Participants(name=form.participant7.data, voteevent=voteevent.id)
			db.session.add(participants)
			db.session.commit()
		if form.participant8.data:
			participants = Participants(name=form.participant8.data, voteevent=voteevent.id)
			db.session.add(participants)
			db.session.commit()
		if form.participant9.data:
			participants = Participants(name=form.participant9.data, voteevent=voteevent.id)
			db.session.add(participants)
			db.session.commit()
		if form.participant10.data:
			participants = Participants(name=form.participant10.data, voteevent=voteevent.id)
			db.session.add(participants)
			db.session.commit()
		form.name.data = ''
		form.description.data = ''
		form.participant1.data = ''
		form.participant2.data = ''
		form.participant3.data = ''
		form.participant4.data = ''
		form.participant5.data = ''
		form.participant6.data = ''
		form.participant7.data = ''
		form.participant8.data = ''
		form.participant9.data = ''
		form.participant10.data = ''
		flash("Event Created Successfully!")
		return redirect(url_for('dashboard'))
	return render_template('createvoteevent.html',firstname=session['firstname'],form=form)

# Create closevoteevent Page
@app.route('/closevoteevent', methods=['GET', 'POST'])
@login_required
def closevoteevent():
	voteevents = Voteevent.query.filter_by(created_by=session['id'],status='open')
	if voteevents.count()>0:
		form = CloseEventForm()
		form.selectedevents.choices = [(event.name) for event in voteevents]
		if form.validate_on_submit():
			for each in form.selectedevents.data:
				voteevent = Voteevent.query.filter_by(name=each).first()
				voteevent.status = "closed"
				db.session.commit()
			form.selectedevents = ''
			flash("Event Closed Successfully!")
			return redirect(url_for('dashboard'))
	else:
		flash("No events created to close!")
		return redirect(url_for('dashboard'))
	return render_template('closevoteevent.html',firstname=session['firstname'],voteevents=voteevents,form=form)

# Create eventaction Page
@app.route('/eventaction/<int:eventid>', methods=['GET', 'POST'])
@login_required
def eventaction(eventid):
	voteevent = Voteevent.query.get_or_404(eventid)
	if voteevent is not None:
		participants = Participants.query.filter_by(voteevent=eventid).order_by(Participants.votecount.desc())
		if voteevent.status == "open":
			voteeventuser = Voteeventuser.query.filter_by(user=session['id'],voteevent=eventid).first()
			if voteeventuser is None:
				#User didn't caste vote for this event
				form = CastVoteForm()
				form.selectedparticipant.choices = [(participant.name) for participant in participants]
				if form.validate_on_submit():
					chosenparticipant = Participants.query.filter_by(name=form.selectedparticipant.data,voteevent=eventid).first()
					chosenparticipant.votecount = int(chosenparticipant.votecount)+1
					db.session.commit()
					voteeventuser = Voteeventuser(user=session['id'],voteevent=eventid,uservoted='True')
					db.session.add(voteeventuser)
					db.session.commit()
					form.selectedparticipant=''
					flash("Vote casted successfully!")
					return redirect(url_for('dashboard'))
				return render_template('eventaction.html',firstname=session['firstname'],voteevent=voteevent, participants=participants,form=form)
			return render_template('eventaction.html',firstname=session['firstname'],voteevent=voteevent, participants=participants)
		else:
			if participants[0].votecount == 0:
				message = "There is no winner for this event!"
			else:
				message = "The winner for this event is "+ participants[0].name
			return render_template('eventaction.html',firstname=session['firstname'],voteevent=voteevent, participants=participants, message=message)
	return render_template('eventaction.html',firstname=session['firstname'])

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

# Create Model
class Users(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), nullable=False, unique=True)
	firstname = db.Column(db.String(200), nullable=False)
	lastname = db.Column(db.String(200), nullable=False)
	email = db.Column(db.String(120), nullable=False, unique=True)
	gender = db.Column(db.String(10), nullable=False)
	date_added = db.Column(db.DateTime, default=datetime.utcnow)

	# Do some password stuff!
	password_hash = db.Column(db.String(128))


	@property
	def password(self):
		raise AttributeError('password is not a readable attribute!')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	# Create A String
	def __repr__(self):
		return '<Name %r>' % self.name
	
# Create a Participants model
class Participants(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255), nullable=False, unique=True)
	votecount = db.Column(db.Integer, default=0)
	# Foreign Key To Link Users (refer to primary key of the voteevent)
	voteevent = db.Column(db.Integer, db.ForeignKey('voteevent.id'))
	date_added = db.Column(db.DateTime, default=datetime.utcnow)
	
# Create a Voteevent model
class Voteevent(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255), nullable=False, unique=True)
	status = db.Column(db.String(255), nullable=False, default='open')
	description = db.Column(db.Text)
	date_added = db.Column(db.DateTime, default=datetime.utcnow)
	created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
	
# Create a Voteeventuser model
class Voteeventuser(db.Model):
	id = db.Column(db.Integer, primary_key=True)    
    # Foreign Key To Link Users (refer to primary key of the user)
	user = db.Column(db.Integer, db.ForeignKey('users.id'))
	# Foreign Key To Link Users (refer to primary key of the voteevent)
	voteevent = db.Column(db.Integer, db.ForeignKey('voteevent.id'))
	uservoted = db.Column(db.String(10), nullable=False, default='False')