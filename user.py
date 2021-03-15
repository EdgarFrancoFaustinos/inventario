from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin):
    """ Esta clase nos sirve para crear nuevos usuarios y utilizar sus metodos """
    def __init__(self, id, name, email, password, is_admin=False):
        self.id = id
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.is_admin = is_admin

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.email)


users = []
alex = User(1, 'alex', 'alex@gmail.com', '123')
users.append(alex)

def get_user(email):
    for user in users:
        if user.email == email:
            return user
    return None
