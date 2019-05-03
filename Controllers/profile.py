from flask import Blueprint, session, render_template, request, Response, send_from_directory
from Models.Models import User, Portfolio, PassportData
from app import *
from werkzeug.utils import secure_filename
import os

profile_controller = Blueprint('profile_controller', __name__, template_folder='templates')



@profile_controller.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'GET':
        user_tuple = ['tester@tester.com', '12312312', 'null']

        if session.get('user') is not None:
            user_tuple = session.get('user')
        user = User(user_tuple[0], user_tuple[1])
        data = user.get_info()
        data['birthday'] = data['birthday'].strftime('%d.%m.%Y')
        return render_template('profile.html', data=data)
    else:
        user_tuple = ['tester@tester.com', '12312312', 'null']

        if session.get('user') is not None:
            user_tuple = session.get('user')

        user = User(user_tuple[0], user_tuple[1])
        data = request.get_json(silent=True)
        print(data)
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

        if session.get('user') is not None:
            user_tuple = session.get('user')
        user = User(user_tuple[0], user_tuple[1])
        data = user.contacts()
        print(data)
        return render_template('contacts.html', data=data)
    else:
        user_tuple = ['tester', '12312312', 'null']

        if session.get('user') is not None:
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
        if session.get('user') is not None:
            username = session.get('user')[0]
        ins = PassportData(username)
        data = ins.retrieve()
        data = ins.get_data_without_db()
        print(data)
        return render_template('passport.html', data=data)
    else:
        data = request.get_json(silent=True)

        if session.get('user') is None:
            username = data['username']  #
        else:
            username = session.get('user')[0]
        passport = PassportData(username=username)
        print(data)
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


@profile_controller.route('/education', methods=['GET', 'POST'])
def education():
    if request.method == 'POST':
        data = request.get_json(silent=True)
    else:
        data = {"0": {"input": "KSMS", "date": "20.06.2017"},
                "1": {"input": "KSMS", "date": "20.06.2017"}}
        return render_template('education.html', data=data)


@profile_controller.route('/add_attachment', methods=['GET', 'POST'])
def add_attachment():
    if request.method == 'POST':
        data = request.get_json(silent=True)
        username = 'tester@tester.com'

        if session.get('user') is not None:
            username = session.get('user')[0]
        print(data)
        attachment = data['attachment']
        # print(attachment_binary)
        # name_of_attachment = data['name_of_attachment']
        user_portfolio = Portfolio(username)
        user_portfolio.insert_file(attachment)
        return Response('added attachment successfully')
    else:
        username = 'tester@tester.com'

        if session.get('user') is not None:
            username = session.get('user')[0]
        user_portfolio = Portfolio(username)
        data = user_portfolio.retrieve()

        print(data)

        return Response('got the picture')


@profile_controller.route('/profile_picture', methods=['POST', 'GET'])
def profile_picture():
    # return Response('added photo successfully')
    if request.method == 'POST':
        data = request.get_json(silent=True)
        print(data)
        user_data = session.get('user')
        if user_data is None:
            user_data = 'tester@tester.com'
        user = User(user_data[0])
        user.add_photo(data['photo_binary'], user.username)

        return Response('added photo successfully')
    else:
        username = "tester@tester.com"

        if session.get('user') is not None:
            username = session.get('user')[0]

        # now we are going to retrieve data from the db
        user = User(username)
        user.get_photo(username)
        return Response(b'got the picture')
        # add some template
