from flask import Flask, redirect, render_template, request, Response, url_for, jsonify

from Models import User

app = Flask(__name__)


def hash_password(password: str) -> str:
	from hashlib import md5
	return md5(password.encode()).hexdigest()


@app.route('/')
def hello_world():
	return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		data = request.get_json(silent=True)
		password = hash_password(data['password'])
		user = User(data['username'], password)
		if user.verify():
			return jsonify(dict(redirect=url_for("profile", username=data['username'])))
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
			return jsonify(dict(redirect=url_for("profile", username=email)))
		else:
			return Response("Password are not the same!")
	return render_template('registration.html')

@app.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username=None):
	return render_template('profile.html', username=username)

if __name__ == '__main__':
	app.run()
