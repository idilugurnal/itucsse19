from flask import Flask, jsonify,render_template, url_for, flash , redirect, request, abort,request, current_app, send_from_directory
from flask_login import LoginManager
from flask_login.utils import login_required, login_user, current_user, logout_user
from dbconn import Database
from flask_bcrypt import Bcrypt
import forms
from user import User
from dbconn import ConnectionPool


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
        return render_template("university_student.html")
    elif user.userType == "High School Student":
        return render_template("hschool_student.html")
    elif user.userType == "University Representative" or user.userType == "High School Representative" :
        print("heyy");
        return render_template("rep_home_page.html", posts = user )
    else:
        return render_template("home.html")


@app.route("/CreateEvent/<type>", methods=['GET' , 'POST'])
@login_required
def create_event(type):
    if type == "University Representative":
        pass
        #TODO: create Event class and add event to database
    else:
        #TODO: Implement error here
        return render_template("home.html")



@app.route('/register', methods=['GET' , 'POST'])
def register():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        my_user = User(form.name.data, form.surname.data, form.username.data, form.email.data, hashed_pass, form.institution.data, form.user_type.data)
        try:
            my_user.save_to_db()
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
            print(new_user.userType)
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


if __name__ == '__main__':
    app.run()


