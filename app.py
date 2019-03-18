from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
from Models import User

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User(request.form['username'], request.form['password'])
        if user.verify():
            return "Success!"
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User()
        name = request.form['name']
        sname = request.form['sname']
        email = request.form['email']
        bdate = request.form['birthday']
        if request.form['password'] == request.form['cpassword']:
            password = request.form['password']
            # user.register(email, password, name, sname, email,bdate)
            return "Success"
        else:
            return "Incorrect Username or Password"
    return render_template('registration.html')


if __name__ == '__main__':
    app.run()

a = int(input())
b = int(input())
if a > b:
    print(a)
else:
    print(b)
