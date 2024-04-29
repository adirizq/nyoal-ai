import os
import sys
import utils

from dotenv import load_dotenv
from flask import Flask, render_template

from views import views


load_dotenv(override=True)

os.makedirs('export', exist_ok=True)

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.getenv('SECRET_KEY')


utils.init_login_manager(app)


for view in views:
    app.register_blueprint(view)


@app.route('/')
def index():
    return render_template('front/index.html')