from flask import Flask, redirect, render_template, request, json, Response, jsonify, session, send_from_directory
from Models import User, PassportData
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.secret_key = 'xyz'
TESTING = False
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
        data['password'] = hash_password(data['password'])
        user = User(data['username'], data['password'])
        if user.verify():
            session['user'] = (user.username, user.password)
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


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'GET':
        user_tuple = ['tester', '12312312', 'null']
        if not TESTING:
            user_tuple = session.get('user')
        user = User(user_tuple[0], user_tuple[1])
        data = user.get_info()
        data['birthday'] = data['birthday'].strftime('%d.%m.%Y')
        return render_template('profile.html', data=data)
    else:
        user_tuple = ['tester', '12312312', 'null']
        if not TESTING:
            user_tuple = session.get('user')

        user = User(user_tuple[0], user_tuple[1])
        data = request.get_json(silent=True)
        fname = data['fname']
        sname = data['sname']
        bdate = data['bdate']
        gender = data['gender']
        citizenship = data['citizenship']
        user.update_info(fname, sname, bdate, gender, citizenship)
        return Response('Basic info successfully created')


@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    if request.method == 'GET':

        user_tuple = ['tester', '12312312', 'null']
        if not TESTING:
            user_tuple = session.get('user')
        user = User(user_tuple[0], user_tuple[1])
        data = user.contacts()
        return render_template('contacts.html', data=data)
    else:
        user_tuple = ['tester', '12312312', 'null']
        if not TESTING:
            user_tuple = session.get('user')
        user = User(user_tuple[0], user_tuple[1])
        data = request.get_json(silent=True)
        user.update_contacts(data['index'], data['region'], data['city'], data['street'],
                             data['building'], data['corpus'], data['flat'])
        return Response('Successfully updated!')


@app.route('/passport', methods=['GET', 'POST'])
def passport():
    if request.method == 'GET':
        username = "tester"
        if not TESTING:
            username = session.get('user')[0]
        data = PassportData(username).retrieve()
        return render_template('passport.html')
    else:
        data = request.get_json(silent=True)
        username = data['username']  #
        passport = PassportData(username=username)
        passport.register(passport_series=data['passport_series'], passport_num=data['passport_number'],
                          issue_date=data['issue_date'], issuing_authority=data['issuing_authority'])
        return Response('Success')


@app.route('/education')
def education():
    return render_template('education.html')

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
