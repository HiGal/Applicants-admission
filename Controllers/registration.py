from flask import Blueprint, request, Response, render_template
from Models.Models import User
from Security.Secure import hash_password

registration_controller = Blueprint('registration_controller', __name__, template_folder='templates')


@registration_controller.route('/register', methods=['GET', 'POST'])
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
