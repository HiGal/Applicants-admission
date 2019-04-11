from flask import Blueprint, session, render_template, request, Response
from Models.Models import User, PassportData

profile_controller = Blueprint('profile_controller', __name__, template_folder='templates')


@profile_controller.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'GET':
        user_tuple = session.get('user')
        user = User(user_tuple[0], user_tuple[1])
        data = user.get_info()
        data['birthday'] = data['birthday'].strftime('%d.%m.%Y')
        return render_template('profile.html', data=data)
    else:
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
        user_tuple = session.get('user')
        user = User(user_tuple[0], user_tuple[1])
        data = user.contacts()
        return render_template('contacts.html', data=data)
    else:
        user_tuple = session.get('user')
        user = User(user_tuple[0], user_tuple[1])
        data = request.get_json(silent=True)
        user.update_contacts(data['index'], data['region'], data['city'], data['street'],
                             data['building'], data['corpus'], data['flat'])
        return Response('Successfully updated!')


@profile_controller.route('/passport', methods=['GET', 'POST'])
def passport():
    if request.method == 'GET':
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


@profile_controller.route('/education')
def education():
    return render_template('education.html')
