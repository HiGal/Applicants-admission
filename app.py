from flask import Flask, redirect, render_template, request, json, Response, jsonify, session
from Models import User

app = Flask(__name__)
app.secret_key = 'xyz'


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
        session['user'] = (data['username'], data['password'])
        if user.verify():
            return Response('/profile')
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
            password = hash_password(data['password'])
            user.register(email, password, name, sname, email, bdate)
            return Response("Account successfully created")
        else:
            return Response("Password are not the same!")
    return render_template('registration.html')


@app.route('/profile')
def profile():
    user_tuple = session.get('user')
    user = User(user_tuple[0], user_tuple[1])
    data = user.get_info()
    data['birthday'] = data['birthday'].strftime('%d-%m-%yyyy')
    return render_template('profile.html', data=data)


@app.route('/contacts')
def contacts():
    tuple = session.get('user')
    user = User(tuple[0], tuple[1])
    return jsonify(user.contacts())


@app.route('/edit-profile-info', methods=['GET', 'POST'])
def edit_profile_info():
    if request.method == 'POST':
        data = request.get_json(silent=True)
        tuple = session.get('user')
        user = User(tuple[0], tuple[1])
        name = data['name']
        sname = data['sname']
        citizenship = data['citizenship']
        bdate = data['bdate']
        gender = data['gender']
        user.update_personal_info(name, sname, citizenship, bdate, gender)
    return render_template('profile.html')


if __name__ == '__main__':
    app.run()
