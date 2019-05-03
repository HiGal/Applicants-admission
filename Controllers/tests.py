from flask import Blueprint, session, render_template, request, Response,jsonify
import random
from Models.Models import *

tests_controller = Blueprint('tests_controller', __name__, template_folder='templates')


@tests_controller.route('/add_test', methods=['POST'])
def add_test():
    data = request.get_json(silent=True)
    question = data['question']
    choice1 = data['choice1']
    choice2 = data['choice2']
    choice3 = data['choice3']
    choice4 = data['choice4']
    correct_choice = data['choice1']
    arr = [choice1, choice2, choice3, choice4]
    random.shuffle(arr)
    choice1 = arr[0]
    choice2 = arr[1]
    choice3 = arr[2]
    choice4 = arr[3]

    username = 'tester@tester.com'
    if session.get('user') is not None:
        username = session.get('user')[0]
    test = Test(username)
    test.insert_test(question, choice1, choice2, choice3, choice4, correct_choice)
    return Response('Test added successfully')


@tests_controller.route('/add_test', methods=['GET'])
def get_the_test():
    data = {
        'question': '',
        'choice1': '',
        'choice2': '',
        'choice3': '',
        'choice4': ''
    }
    return render_template('add_test.html', data=data)



@tests_controller.route('/tests', methods=['GET'])
def tests_page():
    return render_template('tests.html')


@tests_controller.route('/get_tests', methods=['GET'])
def fetch_date():
    username = 'tester@tester.com'
    testing = True
    if session.get('user') is not None:
        testing = False
        username = session.get('user')[0]
    test = Test(username)
    data = test.get_tests()
    print(data)
    if not testing:
        return jsonify(data)
    return b'data fetched correctly'


@tests_controller.route('/update_result', methods=['POST'])
def update_result():
    username = 'tester@tester.com'
    data = request.get_json(silent=True)
    if session.get('user') is not None:
        username = session.get('user')
    portfolio = Portfolio(username=username)
    portfolio.insert_result(result=data['result'])
    return b'successfully updated the result'
