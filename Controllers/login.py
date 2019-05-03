from flask import Blueprint, redirect, Response, render_template, session, request
from Models.Models import User
from Security.Secure import hash_password

login_controller = Blueprint('login_controller', __name__, template_folder='templates')


@login_controller.route('/')
def hello_world():
    return redirect("/login")


@login_controller.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json(silent=True)
        data['password'] = hash_password(data['password'])
        user = User(data['username'], data['password'])
        #print(user.verify())

        if user.verify():
            session['user'] = (user.username, user.password)
            if user.get_type() == 'professor':
                return Response('/professor')
            return Response('/profile')
        else:
            return Response("Username or Password incorrect")
    return render_template('login.html')

