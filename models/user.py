from flask_login import UserMixin

from firebase_config import firebase_db
from firebase_admin import firestore

class User(UserMixin):
    def __init__(self, id, name, email, is_admin, is_banned=False):
        self.id = id
        self.name = name
        self.email = email
        self.is_admin = is_admin
        self.is_banned = is_banned

    def __repr__(self):
        role_string = 'Admin' if self.is_admin else 'User'
        return f'<User: {self.name} | {self.email} | {role_string}>'
    
    def update(self):
        firebase_db.collection('users').document(self.id).update({
            'name': self.name,
            'email': self.email,
            'is_admin': self.is_admin,
            'is_banned': self.is_banned
        })

        return self
    
    @staticmethod
    def get_all():
        users = firebase_db.collection('users').stream()
        list_users = []

        for user in users:
            list_users.append(User(user.id, user.to_dict()['name'], user.to_dict()['email'], user.to_dict()['is_admin'], False if 'is_banned' not in user.to_dict() else user.to_dict()['is_banned']))

        return list_users
    

    @staticmethod
    def get_by_id(user_id):
        user = firebase_db.collection('users').document(user_id).get()
        return User(user.id, user.to_dict()['name'], user.to_dict()['email'], user.to_dict()['is_admin'], False if 'is_banned' not in user.to_dict() else user.to_dict()['is_banned'])