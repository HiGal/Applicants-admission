from flask import Flask

from Controllers.login import login_controller
from Controllers.professor_profile import professor_controller
from Controllers.profile import profile_controller
from Controllers.registration import registration_controller
from Controllers.tests import tests_controller

UPLOAD_FOLDER = 'D:/lectures/Software Project/dev/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'xyz'
app.register_blueprint(login_controller)
app.register_blueprint(registration_controller)
app.register_blueprint(profile_controller)
app.register_blueprint(tests_controller)
app.register_blueprint(professor_controller)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB



TESTING = True

if __name__ == '__main__':
    app.run()
