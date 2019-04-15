from flask import Flask, redirect, render_template, request, Response, session
from Controllers.login import login_controller
from Controllers.registration import registration_controller
from Controllers.profile import profile_controller

import os
from flask import Flask, redirect, render_template, request, json, Response, jsonify, session, send_from_directory
from Models.Models import User, PassportData, Portfolio

UPLOAD_FOLDER = 'D:/lectures/Software Project/dev/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.secret_key = 'xyz'
app.register_blueprint(login_controller)
app.register_blueprint(registration_controller)
app.register_blueprint(profile_controller)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB


def hash_password(password: str) -> str:
    from hashlib import md5
    return md5(password.encode()).hexdigest()


TESTING = True


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
        username = "tester@tester.com"
        if not TESTING:
            username = session.get('user')[0]
        data = PassportData(username).retrieve()
        return render_template('passport.html', data=data)
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


@app.route('/profile_picture', methods=['POST', 'GET'])
def profile_picture():
    # return Response('added photo successfully')
    if request.method == 'POST':
        data = request.get_json(silent=True)
        user = User(data['username'])
        user.add_photo(data['photo_extension'], data['photo_binary'], data['byte_count'], user.username)

        return Response('added photo successfully')
    else:
        username = "tester@tester.com"
        if not TESTING:
            username = session.get('user')[0]

        # now we are going to retrieve data from the db
        user = User(username)
        data = user.get_photo(username)

        # PAY ATTENTION THAT DATA HERE IS
        #  data = {photo_integer, byte_count}
        #
        return Response(b'got the picture')
        # add some template


@app.route('/add_attachment', methods=['GET', 'POST'])
def add_attachment():
    if request.method == 'POST':
        data = request.get_json(silent=True)
        username = 'tester@tester.com'
        if not TESTING:
            username = session.get('user')[0]
        attachment_integer = data['attachment_integer']
        #print(attachment_binary)
        # name_of_attachment = data['name_of_attachment']
        user_portfolio = Portfolio(username)
        user_portfolio.insert_file(attachment_integer, data['byte_count'])

        return Response('added attachment successfully')
    else:
        username = 'tester@tester.com'
        if not TESTING:
            username = session.get('user')[0]
            user_portfolio = Portfolio(username)
            data = user_portfolio.retrieve()
        return Response('got the picture')


# @app.route('/portfolio', methods=['GET','POST'])
# def portfolio():
#     if request.method == 'POST':
#         data = request.get_json(silent=True)
#         print(data['pdf'])
#         return Response(data['pdf'])
#     else:
#         return render_template('portfolio.html')


if __name__ == '__main__':
    app.run()
