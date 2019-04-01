from flask import Flask, redirect, render_template, request, json, Response
from Models import User

app = Flask(__name__)


def hash_password(password: str) -> str:
    from hashlib import md5
    return md5(password.encode()).hexdigest()


@app.route('/')
def hello_world():
    return redirect("/login")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json(silent=True)
        user = User(data['username'], data['password'])
        if user.verify():
            return Response("Success!")
        else:
            return Response("Username or Password incorrect")
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User()
        data = request.get_json(silent=True)
        name = data['name']
        sname = data['sname']
        email = data['email']
        bdate = data['bdate']
        if data['password'] == data['cpassword']:
            password = data['password']
            user.register(email, password, name, sname, email, bdate)
            return Response("Account successfully created")
        else:
            return Response("Password are not the same!")
    return render_template('registration.html')


@app.route('/personal-info', methods=['GET','POST'])
def update_info():  # In front end there should be added multiple checkers for and all these labels are required
    if request.method == 'POST':
        user = User()
        data = request.get_json(silent=True)
        username = data['username']
        fname = data['fname']
        sname = data['sname']
        bdate = data['bdate']
        gender = data['gender']
        citizenship = data['citizenship']
        user.update_info(username, fname, sname, bdate, gender, citizenship)

        return Response('Basic info successfully created')
    return render_template('personal_info.html')






if __name__ == '__main__':
    app.run()
