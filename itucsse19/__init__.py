from flask import Flask, jsonify,render_template, url_for, flash , redirect, request, abort,request, current_app, send_from_directory
from flask_login import LoginManager
from flask_login.utils import login_required, login_user, current_user, logout_user
from dbconn import Database
from flask_bcrypt import Bcrypt
import forms
from user import User


app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = '0fe07ce1917042a7119c446dfa541a05'

#Database.initialise()


@app.route('/', methods=['GET' , 'POST'])
def home_page():
    payload = {'message': 'Hello, world'}
    return jsonify(payload)

@app.route('/register', methods=['GET' , 'POST'])
def register():
    form = forms.RegistrationForm()
    print(form.email.data)
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        my_user = User(form.name.data, form.surname.data, form.username.data, form.email.data, form.password.data, form.institution.data, form.user_type.data)
        try:
            my_user.save_to_db()
        except:
            flash('An error occured!')
            return redirect(url_for("register"))
        flash(f'Your account is created with username {form.username.data}!', 'success')
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form )

@app.route('/login', methods=['GET' , 'POST'])
def login():
    pass


if __name__ == '__main__':
    app.run()


