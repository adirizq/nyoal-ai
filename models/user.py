from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id, name, email, is_admin):
        self.id = id
        self.name = name
        self.email = email
        self.is_admin = is_admin

    def __repr__(self):
        role_string = 'Admin' if self.is_admin else 'User'
        return f'<User: {self.name} | {self.email} | {role_string}>'
    