from models.tag import Tag

from flask import Blueprint, render_template, redirect, flash, request, url_for
from flask_login import login_required, current_user

tag = Blueprint('tag', __name__, template_folder='templates', url_prefix='/dashboard/tag')


@tag.route('/create', methods=['POST'])
@login_required
def create():
    name = request.form['name']
    color = request.form['color']

    try:
        tag = Tag(name, color)
        tag.save(current_user)

        flash('Tag berhasil dibuat', 'success')
        return redirect(url_for('dashboard.tag'))

    except Exception as e:
        print('[ERROR] [CREATE TAG]: ', e)
        flash('Terjadi kesalahan server saat membuat tag', 'error')
        return redirect(url_for('dashboard.tag'))


@tag.route('/update', methods=['POST'])
@login_required
def update():
    tag_id = request.form['tag_id']
    name = request.form['name']
    color = request.form['color']

    try:
        tag = Tag.get_by_id(tag_id)
        tag.name = name
        tag.color = color
        tag.update()

        flash('Tag berhasil diperbarui', 'success')
        return redirect(url_for('dashboard.tag'))

    except Exception as e:
        print('[ERROR] [UPDATE TAG]: ', e)
        flash('Terjadi kesalahan server saat memperbarui tag', 'error')
        return redirect(url_for('dashboard.tag'))


@tag.route('/delete', methods=['POST'])
@login_required
def delete():
    tag_id = request.form['tag_id']

    try:
        tag = Tag.get_by_id(tag_id)
        tag.delete()

        flash('Tag berhasil dihapus', 'success')
        return redirect(url_for('dashboard.tag'))
    
    except Exception as e:
        print('[ERROR] [DELETE TAG]: ', e)
        flash('Terjadi kesalahan server saat menghapus tag', 'error')
        return redirect(url_for('dashboard.tag'))