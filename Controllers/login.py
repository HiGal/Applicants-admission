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
        print(user.verify())
        if user.verify():
            session['user'] = (user.username, user.password)
            return Response('/profile')
        else:

            return Response('/wrong_pass')
    return render_template('login.html')


@login_controller.route('/wrong_pass', methods=['GET'])
def wrong_pass():
    return render_template('wrong_pass.html')


@login_controller.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User()
        data = request.get_json(silent=True)
        name = data['name']
        sname = data['sname']
        email = data['email']
        bdate = data['bdate']
        if data['password'] == data['cpassword']:
            password = hash_password(data['password'])
            user.register(email, password, name, sname, email, bdate)
            return Response("Account successfully created")
        else:
            return Response("Password are not the same!")
    return render_template('registration.html')
