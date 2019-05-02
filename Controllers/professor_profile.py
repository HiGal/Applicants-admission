from flask import Blueprint, redirect, Response, render_template, session, request
from Models.Models import User
from Security.Secure import hash_password

professor_controller = Blueprint('professor_controller', __name__, template_folder='templates')


@professor_controller.route('/professor', methods=['GET', 'POST'])
def redirect():
    data = {
        'fname': 'Daniel',
        'sname': ' De Carvalho',
        'bdate': '01-01-1950',
        'citizenship': 'Français',
        'gender': 'M'
    }
    return render_template('professor_page.html', data=data)
