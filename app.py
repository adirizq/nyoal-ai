import os
import sys

from dotenv import load_dotenv
from flask import Flask, render_template

from views import views


load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='templates')

for view in views:
    app.register_blueprint(view)


@app.route('/')
def index():
    return render_template('front/index.html')