from flask_login import LoginManager


login_manager = LoginManager()


def init_login_manager(app):
    login_manager.init_app(app)
    login_manager.login_view = 'auth.sign_in'
    login_manager.login_message = 'Anda harus login untuk mengakses halaman ini'
    login_manager.login_message_category = 'error'