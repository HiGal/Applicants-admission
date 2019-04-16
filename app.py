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

if __name__ == '__main__':
    app.run()
