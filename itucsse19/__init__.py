from flask import Flask, jsonify,render_template, url_for, flash , redirect, request, abort,request, current_app, send_from_directory
from flask_login import LoginManager
from flask_login.utils import login_required, login_user, current_user, logout_user
from dbconn import Database
from flask_bcrypt import Bcrypt
import forms
from institution import  Institution, Address
from dbconn import ConnectionPool
from user import User,Event


app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = '0fe07ce1917042a7119c446dfa541a05'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

Database.initialise()


@app.route('/', methods=['GET' , 'POST'])
def home_page():
    return render_template("home.html")

@app.route("/home", methods=['GET' , 'POST'])
@login_required
def user_home_page():
    user = User.get_by_username(current_user.username)
    print(user.userType)
    if user.userType == "University Student":
        events = User.get_institution_events(current_user)
        return render_template("university_student.html", events=events)
    elif user.userType == "High School Student":
        return render_template("hschool_student.html")
    elif user.userType == "University Representative" or user.userType == "High School Representative" :
        return render_template("rep_home_page.html", posts = user )
    else:
        return render_template("home.html")


@app.route('/register', methods=['GET' , 'POST'])
def register():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        my_user = User(form.name.data, form.surname.data, form.username.data, form.email.data, hashed_pass, form.institution.data, form.user_type.data)
        try:
            my_user.save_to_db()
            if my_user.userType == "University Representative" or my_user.userType == "High School Representative" :
                institution = Institution.get_by_name(my_user.institution)
                institution.register(my_user.get_id())
        except:
            flash('An error occured!')
            return redirect(url_for("register"))
        flash(f'Your account is created with username {form.username.data}!', 'success')
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form )


@app.route("/login" , methods = ['GET' , 'POST'])
def login():
    form = forms.LoginForm()
    if request.method == 'POST':
        if current_user.get_id() is not None:
            logout_user()

        mail = form.email.data
        password = form.password.data
        new_user = User.get_by_email(mail)
        if new_user and bcrypt.check_password_hash(new_user.password, password):
            login_user(new_user)
            flash(f'Logged in successfuly!' , 'success ')
            return redirect(url_for('user_home_page'))
        else:
            flash('Email or password incorrect')
            return render_template("login.html" , title = "Login" , form = form)
    else:
        if current_user.get_id() is not None:
            logout_user()
        return render_template('login.html', title= "Login" , form = form)


@login_manager.user_loader
def load_user(user_id):
    with ConnectionPool() as cursor:
        cursor.execute('SELECT * FROM user_info WHERE userID = %s', (user_id,))
        user_data = cursor.fetchone()
        if user_data is not None:
            name = user_data[3]
            last_name = user_data[4]
            email = user_data[5]
            hashed_pass = user_data[7]
            institution = user_data[6]
            user_name = user_data[2]
            userID = user_data[0]
            userType = user_data[1]
            user = User(name, last_name, user_name, email, hashed_pass, institution, userType, userID)
            return user
        else:
            return

@app.route("/institution/update", methods=['GET', 'POST'])
@login_required
def update_institution_İnfo():
    # user type kontrol edilmeli
    form = forms.UpdateInsInfoForm()
    user = User.get_by_username(current_user.username)
    posts = Institution.get_by_representative(user.get_id())
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                new_info = Institution(None, user.institution, form.webaddress.data, form.info.data, form.contactInfo.data)
                new_info.update_information();
            except:
                flash('Could not update profile!')
                return redirect(url_for('update_institution_İnfo'))
        flash(f'Institution info is updated successfully!', 'success')
        return redirect(url_for('user_home_page'))
    return render_template("update_institution_info.html", title="Update", form=form, posts = posts)


@app.route("/institution", methods=['GET'])
def profile():
    user = User.get_by_username(current_user.username)
    institution = Institution.get_by_name(user.institution)
    institution.get_addresses()
    return render_template("institution_profile.html", posts = institution)

@app.route("/institution/addresses", methods=['GET', 'POST'])
@login_required
def addresses():
    #user type kontrol edilmeli
    form = forms.AddAddress()
    user = User.get_by_username(current_user.username)
    institution = Institution.get_by_name(user.institution)
    institution.get_addresses()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                new_address=Address(None, institution.institutionID, form.city.data, form.address.data)
                new_address.save_to_db()
            except:
                flash('Could not add the address!')
                return redirect(url_for('addresses'))
        flash(f'New address is added successfully!', 'success')
        return redirect(url_for('addresses'))
    return render_template("addresses.html", posts = institution.addresses, form=form)


@app.route('/institution/delete_address/<address_id>', methods = ['POST'])
@login_required
def delete_address(address_id):
    address_to_delete = Address(address_id, None, None, None)
    address_to_delete.delete_from_db()
    return redirect(url_for('addresses'))


@app.route("/create_event", methods=['GET' , 'POST'])
@login_required
def create_event():
    user = User.get_by_username(current_user.username)
    institution = Institution.get_by_representative(user.get_id())
    institution.get_addresses()
    form = forms.CreateEvent()
    form.address.choices = [(address.address, address.address) for address in institution.addresses]
    if user.userType == "University Representative":
        if request.method == 'POST':
            try:
                event = Event(form.event_name.data, form.info.data, institution.institutionID, "university",
                              form.date.data, form.time.data, form.duration.data, form.venue.data, form.address.data,
                              form.quota.data, form.isOpen.data)
                event.save_to_db(user.id)
                flash('Event is Successfuly Created!', 'success')
                return redirect(url_for("user_home_page"))
            except:
                flash('Event can not be created!')
        return render_template("create_event.html", form=form)
    elif user.userType == "High School Representative":
        if request.method == 'POST':
            try:
                event = Event(form.event_name.data, form.info.data, institution.institutionID, "high school",
                              form.date, form.time, form.duration, form.venue, form.address, form.quota, form.isOpen)
                event.save_to_db(user.id)
                flash('Event is Successfuly Created!', 'success')
                return redirect(url_for("user_home_page"))
            except:
                flash('Event can not be created!')
        return render_template("create_event.html", form=form)
    return redirect(url_for("login"))


@app.route("/volunteer", methods=['POST'])
@login_required
def volunteer():
    event_id = request.form['event_id']
    print(event_id)
    print(current_user.get_id())
    with ConnectionPool() as cursor:
        try:
            cursor.execute("INSERT INTO participants(eventID, participantID) VALUES(%s,%s)" , (event_id, current_user.get_id()))
            flash('Successfuly Volunteered!')
        except:
            flash('An Error Occured')
    return redirect(url_for("user_home_page"))

@app.route("/leaveevent", methods=['POST'])
@login_required
def leave_event():
    event_id = request.form['event_id']
    print(current_user.get_id())
    with ConnectionPool() as cursor:
        try:
            cursor.execute("DELETE FROM participants WHERE eventID = %s" , (event_id, ))
            flash('Left Event!')
        except:
            flash('An Error Occured')
    return redirect(url_for("user_home_page"))


@app.route("/myevents", methods=['GET'])
@login_required
def my_events():
    events = User.get_events(current_user)
    for event in events:
        print(event.id)
    return render_template("myevents.html", events=events)



if __name__ == '__main__':
    app.run()


