import os
import sys

from models.tag import Tag
from models.qa_pack import QAPack
from model_inference import ModelInference

from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from dotenv import load_dotenv


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
    tags = Tag.get_all_dict(current_user)
    qa_packs = QAPack.get_all_for_table(current_user)
    title = 'paket_soal'
    return render_template('dashboard/qa_pack.html', title=title, tags=tags, qa_packs=qa_packs)


@dashboard.route('/tag')
@login_required
def tag():
    tags = Tag.get_all_dict(current_user)
    title = 'tag'
    return render_template('dashboard/tag.html', title=title, tags=tags)