# importamos el modulo models que contiene la clase de la base de datos
from models import DataBase

# libreria para obtener el tiempo mediante la zona horaria
from datetime import datetime
import pytz


class Equipment:

    """ Clase -> Moldea nuevos equipos """
    """Metodo especial constructor ---   __init__   ---"""
    def __init__(self, nombre='', no_serie='', ubicacion="", marca='', estado='', resguardo='',modelo='', observaciones='', barcode=''):
        self.nombre = nombre
        self.no_serie = no_serie
        self.ubicacion = ubicacion
        self.marca = marca
        self.estado = estado
        self.resguardo = resguardo
        self.modelo = modelo
        self.observaciones = observaciones
        self.barcode = barcode
        self.db = DataBase()


    def save(self):
        """ Inserta nuevos equipos en la db """

        register_date = self.register_time() # obtiene la fecha actual

        sql = f"""INSERT INTO `equipos`
        (`nombre`, `no_serie`, `ubicacion`, `marca`, `id_estado`, `modelo`, `observaciones`,  `fecha_registro`, `barcode`, `resguardo`)
        VALUES ('{self.nombre}', '{self.no_serie}', '{self.ubicacion}', '{self.marca}', '{self.estado}', '{self.modelo}', '{self.observaciones}', '{register_date}', '{self.barcode}', '{self.resguardo}'); """

        self.db.execute_query(sql)


    def register_time(self):
        """ Obtiene la fecha y hora acutal de la ciudad de mexico, asi no afecta si se monta a un servidor de EU """

        mex = pytz.timezone('America/Mexico_City')
        datetime_MX = datetime.now(mex)
        register_date = datetime_MX.strftime("%Y-%m-%d %H:%M:%S")

        return register_date


    def get_equipment_info(self, barcode):
        """
        Busca un equipo en la db haciendo match con su barcode, en caso de existir lo retorna
        caso contrario retorna una tupla vacia
        """

        sql = f"""
        SELECT *
        FROM equipos as e
        inner join estado as es
        on es.id_estado = e.id_estado
        WHERE barcode = '{barcode}'
        """

        data = self.db.execute_query(sql)

        if data:
            data = data[0]

            equipment_info = {
                'equipment_id': f'{data[0]}',
                'nombre': f'{data[1]}',
                'no_serie': f'{data[2]}',
                'ubicacion': f'{data[3]}',
                'marca': f'{data[4]}',
                'modelo': f'{data[5]}',
                'id_estado': f'{data[6]}',
                'observaciones': f'{data[7]}',
                'fecha_registro': f'{data[8]}',
                'barcode': f'{data[9]}',
                'resguardo': f'{data[10]}',
                'estado': f'{data[12]}'
            }

            return equipment_info

        return data


    def delete_equipment(self, barcode):
        """ Elimina un equipo de la db buscado por codigo de barras """

        sql = f"DELETE FROM equipos WHERE barcode = '{barcode}' limit 1"
        self.db.execute_query(sql)

        return True


    def update_equipment(self, equipment_id):
        """ Funcion encargada de hacer el update de un equipo en la db """
        # considerar en agregar un campo llamado ultima_modificacion

        sql = f"""
        UPDATE `equipos`
        set nombre = '{self.nombre}',
        no_serie = '{self.no_serie}',
        ubicacion = '{self.ubicacion}',
        marca = '{self.marca}',
        id_estado = '{self.estado}',
        resguardo = '{self.resguardo}',
        modelo = '{self.modelo}',
        observaciones = '{self.observaciones}',
        barcode = '{self.barcode}'
        WHERE id_equipos = '{equipment_id}' limit 1;
        """

        self.db.execute_query(sql)


    def get_all_the_equipments(self, filter=None, chosen_filter=''):
        """ Retorna todos los equipos existentes en la db, y si le mandamos un filtro lo va a buscar por esa keyword """

        if chosen_filter and filter is not None:
            SQL = f"""
            SELECT *
            FROM equipos as e
            inner join estado as es
            on es.id_estado = e.id_estado
            WHERE {filter} LIKE  '%{chosen_filter}%'
            """
        else:
            SQL = """SELECT *
            FROM equipos as e
            inner join estado as es
            on es.id_estado = e.id_estado"""

        data = self.db.execute_query(SQL)

        return data


    def check_if_filter_keyword_exist(self, keyword):
        """
        Función encargada de verificar si el keyword coincide con algun nombre de campo de nuestra tabla equipos
        si esta correctamente escrito devuelve True, si no retorna False por que no existe este campo en la db
        """

        FILTER_LIST = [
            'nombre',
            'no_serie',
            'ubicacion',
            'marca',
            'modelo',
            'estado',
            'fecha_registro',
            'barcode',
            'resguardo'
        ]

        if keyword not in FILTER_LIST:
            return False

        return True
