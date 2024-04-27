from models.user import User

from firebase_config import firebase_db


class Tag():
    def __init__(self, name, color, id=None, owner_id=None):
        self.id = id
        self.owner_id = owner_id
        self.name = name
        self.color = color


    def save(self, user: User):
        _, doc_ref = firebase_db.collection('tags').add({
            'name': self.name,
            'color': self.color,
            'owner_id': user.id
        })

        self.id = doc_ref.id
        self.owner_id = user.id

        return self
    

    def update(self):
        firebase_db.collection('tags').document(self.id).update({
            'name': self.name,
            'color': self.color
        })

        return self
    

    def delete(self):
        firebase_db.collection('tags').document(self.id).delete()

        return self
    

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'color': self.color,
            'owner_id': self.owner_id
        }


    @staticmethod
    def get_all(user: User):
        tags = firebase_db.collection('tags').where('owner_id', '==', user.id).stream()
        return [Tag(tag.to_dict()['name'], tag.to_dict()['color'], id=tag.id, owner_id=tag.to_dict()['owner_id']) for tag in tags]


    @staticmethod
    def get_all_dict(user: User):
        tags = firebase_db.collection('tags').where('owner_id', '==', user.id).stream()
        return [{'id': tag.id, 'name': tag.to_dict()['name'], 'color': tag.to_dict()['color'], 'owner_id': tag.to_dict()['owner_id']} for tag in tags]


    @staticmethod
    def get_by_id(tag_id: str):
        tag = firebase_db.collection('tags').document(tag_id).get()
        return Tag(tag.to_dict()['name'], tag.to_dict()['color'], id=tag.id, owner_id=tag.to_dict()['owner_id'])