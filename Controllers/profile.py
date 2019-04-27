from flask import Blueprint, session, render_template, request, Response, send_from_directory
from Models.Models import User, PassportData
from app import *
from werkzeug.utils import secure_filename
import os

profile_controller = Blueprint('profile_controller', __name__, template_folder='templates')
TESTING = False


@profile_controller.route('/profile', methods=['GET', 'POST'])
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


@profile_controller.route('/contacts', methods=['GET', 'POST'])
def contacts():
    if request.method == 'GET':

        user_tuple = ['tester', '12312312', 'null']
        if not TESTING:
            user_tuple = session.get('user')
        user = User(user_tuple[0], user_tuple[1])
        data = user.contacts()
        print(data)
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


@profile_controller.route('/passport', methods=['GET', 'POST'])
def passport():
    if request.method == 'GET':
        username = "tester"
        if not TESTING:
            username = session.get('user')[0]
        passport_data = PassportData(username)
        passport_data.retrieve()
        return render_template('passport.html', data=passport_data.get_data_without_db())
    else:
        data = request.get_json(silent=True)
        username = data['username']  #
        passport = PassportData(username=username)
        passport.register(passport_series=data['passport_series'], passport_num=data['passport_number'],
                          issue_date=data['issue_date'], issuing_authority=data['issuing_authority'])
        return Response('Success')


@profile_controller.route('/portfolio', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return Response('No file part')
        file = request.files['file']
        if file.filename == '':
            Response('No selected file')
            return Response(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('portfolio.html')
    return render_template('portfolio.html')


@profile_controller.route('/education', methods=['GET','POST'])
def education():
    if request.method == 'POST':
        data = request.get_json(silent=True)
        print(data)
    return render_template('education.html')


@profile_controller.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
