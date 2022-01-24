#login page
from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash # hash user's password and check uniqueness
from .models import User
from . import db 
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth',__name__)

@auth.route('/search')
def search():
    return render_template('search.html', user = current_user)



#check user login function

@auth.route('/login', methods=['GET','POST'])
def login():

    if (request.method ==  'POST'):
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email =email).first()

        if (user):


            if (check_password_hash(user.password, password)):

                flash('welcome to FIAA ' + email, category = 'success')
                login_user(user, remember = True)
                return redirect(url_for('views.home'))

            else:

                flash("incorrect password!! \nPlease try again", category = 'error')

        else:
            flash("The user with that email does not exist. \nPlease sign up to login", category = "error")


    return render_template("login.html", user = current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET','POST'])
def signup():

    if request.method == 'POST':
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        password = request.form.get('password')
        checkpassword = request.form.get('checkpassword')

        user = User.query.filter_by(email = email).first()

        if(user):
            flash("There is already an account with that email. \nPlease login or reset password", category = 'error')

        elif(len(email) < 8):
            flash("email length need to be greater than 8 characters", category = "error")

        elif(len(firstname) < 1 or len(lastname) < 2):
            flash("invalid first name or last name", category = "error")

        elif(len(password) < 8):
            flash("password need to have at least 8 characters \n (at least one letter, one number and one special character)", category = "error")

        elif(password != checkpassword):
            flash("passwords does not match", category = "error")

        else:
            #add new_user and output message
            new_user = User(email = email, firstname = firstname , lastname = lastname , password = generate_password_hash(password, method = "sha256"))
            db.session.add(new_user)
            db.session.commit()
            flash("Account successfully created!", category = "success")
            login_user(new_user, remember = True)
            flash('welcome to FIAA ' + email, category = 'success')
            return redirect(url_for('views.home'))

    return render_template("signup.html", user = current_user)