import os
import sys

from flask import Blueprint, render_template
from flask_login import login_required

qa_pack = Blueprint('qa_pack', __name__, template_folder='templates', url_prefix='/dashboard/qa_pack')


@qa_pack.route('/detail/<int:id>')
@login_required
def detail(id):
    title = 'paket_soal'
    return render_template('dashboard/qa_pack_detail.html', title=title, id=id)