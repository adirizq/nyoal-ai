import os
import sys

from flask import Blueprint, render_template


auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/sign-in')
def sign_in():
    return render_template('front/auth/sign_in.html')


@auth.route('/sign-up')
def sign_up():
    return render_template('front/auth/sign_up.html')


@auth.route('/forgot-password')
def forgot_password():
    return render_template('front/auth/forgot_password.html')
