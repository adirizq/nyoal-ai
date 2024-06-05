from models.user import User

from flask import Blueprint, render_template, redirect, flash, request, url_for
from flask_login import login_required, current_user

user = Blueprint('user', __name__, template_folder='templates', url_prefix='/dashboard/user')



@user.route('/update', methods=['POST'])
@login_required
def update():
    user_id = request.form['user_id']
    role = request.form['role']

    try:
        user = User.get_by_id(user_id)
        user.is_admin = True if role == 'admin' else False
        user.update()

        flash('User berhasil diperbarui', 'success')
        return redirect(url_for('dashboard.user'))

    except Exception as e:
        print('[ERROR] [UPDATE USER]: ', e)
        flash('Terjadi kesalahan server saat memperbarui user', 'error')
        return redirect(url_for('dashboard.user'))
    

@user.route('/toggle-ban', methods=['POST'])
@login_required
def toggle_ban():
    user_id = request.form['user_id']

    try:
        user = User.get_by_id(user_id)
        user.is_banned = not user.is_banned
        user.update()

        flash('User berhasil diperbarui', 'success')
        return redirect(url_for('dashboard.user'))

    except Exception as e:
        print('[ERROR] [TOGGLE BAN USER]: ', e)
        flash('Terjadi kesalahan server saat memperbarui user', 'error')
        return redirect(url_for('dashboard.user'))