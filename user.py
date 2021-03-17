# se importa el modulo que nos ayuda con el login de usuario, nuestra clase User hereda de UserMixin
from flask_login import UserMixin

# Este modulo nos ayuda con la seguridad de nuestras contraseñas, las encripta y las desencripta
from werkzeug.security import check_password_hash

# Importamos del archivo models.py la clase DataBase para hacer consultas a la db desde aqui
from models import DataBase


class User(UserMixin):
    """ Esta clase nos sirve para crear nuevos usuarios y utilizar sus metodos """

    def __init__(self, id='', name='', email='', password='', is_admin=False):
        """ Metodo constructor, son los parametros minimos para moldear un usuario """
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.is_admin = is_admin
        self.db = DataBase()

    def check_password(self, password):
        """ Esta funcion verifica que la contraseña del usuario en la db sea la que nos proporcionaron desde el
            template login, recibe como parametro la contraseña y
            retorna True si coincide o False si no coincide """
        return check_password_hash(self.password, password)

    def __repr__(self):
        """ cuando se llama a esta clase retorna el email del usuario, para no retornar un objeto clase """
        return '<User {}>'.format(self.email)

    def get_user(self, email):
        """ Esta funcion verifica que exista el usuario en la db, si es asi retorna el objeto usuario
            en caso contrario retorna None y ya no tiene caso verificar la contraseña
        """

        sql = f"SELECT * FROM usuario where username = '{email}' "
        data = self.db.execute_query(sql)

        if data and data[0][2] == email:
            user = User(data[0][0], data[0][1], data[0][2], data[0][3])
            return user

        return None

    def get_user_by_id(self, user_id):
        """ Esta funcion, se encarga de retornar el usuario buscandolo por ID, de este modo si el usuario no cierra
            sesion, lo volvera a cargar sin pedir credenciales.
        """

        sql = f"SELECT * FROM usuario where id_usuario = '{user_id}' "
        data = self.db.execute_query(sql)

        if data and data[0][0] == user_id:
            user = User(data[0][0], data[0][1], data[0][2], data[0][3])
            return user

        return None
