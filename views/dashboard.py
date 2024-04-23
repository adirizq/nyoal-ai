import os
import sys

from flask import Blueprint, render_template
from flask_login import login_required


dashboard = Blueprint('dashboard', __name__, template_folder='templates', url_prefix='/dashboard')


@dashboard.route('/')
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