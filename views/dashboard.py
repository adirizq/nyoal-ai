import os
import sys

from model_inference import ModelInference
from dotenv import load_dotenv

from flask import Blueprint, render_template, request
from flask_login import login_required

load_dotenv()

dashboard = Blueprint('dashboard', __name__, template_folder='templates', url_prefix='/dashboard')

model_inference = ModelInference(
    project_id=os.getenv('MODEL_PROJECT_ID'),
    endpoint_id=os.getenv('MODEL_END_POINT_ID'),
)

@dashboard.route('/', methods=['GET', 'POST'])
@login_required
def index():
    title = 'uji_coba'
    return render_template('dashboard/index.html', title=title)


@dashboard.route('/qa-pack')
@login_required
def qa_pack():
    title = 'paket_soal'
    return render_template('dashboard/qa_pack.html', title=title)


@dashboard.route('/tag')
@login_required
def tag():
    title = 'tag'
    return render_template('dashboard/tag.html', title=title)