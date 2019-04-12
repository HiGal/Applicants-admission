from flask import Flask, redirect, render_template, request, json, Response, jsonify, session, send_from_directory
from Models import User
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.secret_key = 'xyz'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16 MB

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

@app.route('/portfolio', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return Response('No file part')
        file = request.files['file']
        if file.filename == '':
            Response('No selected file')
            return Response(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('portfolio.html')
    return render_template('portfolio.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run()
