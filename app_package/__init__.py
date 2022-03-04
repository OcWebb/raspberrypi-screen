from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = 'super secret key'
app.config['UPLOAD_FOLDER'] = "/static/images"

from app_package import routes