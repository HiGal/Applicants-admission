from flask import Blueprint, session, render_template, request, Response, send_from_directory
from Models.Models import *
from app import *
from werkzeug.utils import secure_filename
import os

tests_controller = Blueprint('tests_controller', __name__, template_folder='templates')


@tests_controller.route('/add_test', methods=['POST'])
def add_test():
    data = request.get_json(silent=True)
    question = data['question']
    choice1 = data['choice1']
    choice2 = data['choice2']
    choice3 = data['choice3']
    choice4 = data['choice4']
    correct_choice = data['correct_choice']
    username = 'tester@tester.com'
    if session.get('user') is not None:
        username = session.get('user')[0]
    test = Test(username)
    test.insert_test(question, choice1, choice2, choice3, choice4, correct_choice)
    return Response('Test added successfully')


@tests_controller.route('/get_test', methods=['GET'])
def fetch_tests():
    username = 'tester@tester.com'
    if session.get('user') is not None:
        username = session.get('user')[0]
    test = Test(username)
    data = test.get_tests()

    # render_template("sometemplate", data)
    return render_template('tests.html', data=data)
