from flask import Flask, redirect, render_template, request, Response, session
from Controllers.login import login_controller
from Controllers.registration import registration_controller
from Controllers.profile import profile_controller
from Models.Models import User
from Models.Models import PassportData

app = Flask(__name__)
app.secret_key = 'xyz'
app.register_blueprint(login_controller)
app.register_blueprint(registration_controller)
app.register_blueprint(profile_controller)

if __name__ == '__main__':
    app.run()
