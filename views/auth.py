import os
import sys

from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_user, logout_user, current_user

from firebase_config import firebase_auth, firebase_db
from utils import login_manager
from models.user import User


auth = Blueprint('auth', __name__, template_folder='templates')


@login_manager.user_loader
def load_user(user_id):

    if not user_id:
        return None
    
    try:
        user_data = firebase_db.collection('users').document(user_id).get().to_dict()
        user = User(user_id, user_data['name'], user_data['email'], user_data['is_admin'])
        return user
    
    except Exception as e:
        return None


@login_manager.request_loader
def request_loader(request):
    user_id = request.form.get('user_id')

    user = load_user(user_id)
    
    if user:
        return user

    return None


@auth.route('/sign-in', methods=['GET', 'POST'])
def sign_in():

    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if not email or not password:
            flash('Email dan password harus diisi', 'error')
            return render_template('front/auth/sign_in.html')

        try:
            user_docs = firebase_auth.sign_in_with_email_and_password(email, password)
        except:
            flash('Email atau password salah', 'error')
            return render_template('front/auth/sign_in.html')
        
        user_id = user_docs['localId']

        user = load_user(user_id)

        if user:
            login_user(user)
            return redirect(url_for('dashboard.index'))
        
        flash('Email atau password salah', 'error')
        return render_template('front/auth/sign_in.html')

    return render_template('front/auth/sign_in.html')


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if not name or not email or not password or not confirm_password:
            flash('Semua field harus diisi', 'error')
            return render_template('front/auth/sign_up.html')

        if password != confirm_password:
            flash('Password dan konfirmasi password tidak sama', 'error')
            return render_template('front/auth/sign_up.html')

        try:
            user = firebase_auth.create_user_with_email_and_password(email, password)
            user_id = user['localId']

            data = {
                'name': name,
                'email': email,
                'is_admin': False
            }

            firebase_db.collection('users').document(user_id).set(data)

            flash('Akun berhasil dibuat', 'success')
            return redirect(url_for('auth.sign_in'))
        
        except Exception as e:
            flash(e, 'error')
            return render_template('front/auth/sign_up.html')
        
    return render_template('front/auth/sign_up.html')


@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        email = request.form['email']

        if not email:
            flash('Email harus diisi', 'error')
            return render_template('front/auth/forgot_password.html')

        try:
            firebase_auth.send_password_reset_email(email)
            flash('Email reset password telah dikirim', 'success')
            return redirect(url_for('auth.sign_in'))
        
        except Exception as e:
            flash(e, 'error')
            return render_template('front/auth/forgot_password.html')
    
    return render_template('front/auth/forgot_password.html')


@auth.route('/sign-out', methods=['GET', 'POST'])
def sign_out():
    logout_user()
    return redirect(url_for('auth.sign_in'))
