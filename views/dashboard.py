import os
import sys

from flask import Blueprint, render_template


dashboard = Blueprint('dashboard', __name__, template_folder='templates', url_prefix='/dashboard')


@dashboard.route('/')
def index():
    title = 'uji_coba'
    return render_template('dashboard/index.html', title=title)


@dashboard.route('/tag')
def tag():
    title = 'tag'
    return render_template('dashboard/tag.html', title=title)