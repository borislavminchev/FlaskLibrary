from flask import render_template, redirect, url_for, abort, request, Blueprint, Response

from http import HTTPStatus
from flask_login import LoginManager, login_user, logout_user, login_required

from src.db.entity import User
from src.db.service import UserService
from src.controller.views.application import index


login_manager = LoginManager()
auth = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(user_id:str) -> User | None:
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    if request.blueprint == "api":
        abort(HTTPStatus.UNAUTHORIZED)
    return redirect(url_for('auth.login'))

@auth.route('/signup')
def signup() -> str:
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    
    # code to validate and add user to database goes here
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        return redirect(url_for('auth.signup'))
    if not username or not email or not password:
        return {"result": False, "message": "Invalid register data"}
    
    s = UserService().register_user(username=username, email=email, password=password)


    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET': return render_template('login.html')

    email = request.form.get('email')
    password = request.form.get('password')
    # remember = True if request.form.get('remember') else False

    user:User | None = User.query.filter_by(email=email).first()

    if not user or user.password != password:
        return redirect(url_for('auth.login')) 
    
    login_user(user, remember=True)
    return redirect(url_for('index.profile'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index.homescreen'))