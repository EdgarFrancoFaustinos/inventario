# importamos el modulo models que contiene la clase de la base de datos
from models import DataBase

# libreria para obtener el tiempo mediante la zona horaria
from datetime import datetime
import pytz


class Equipment: 

    """ Clase -> Moldea nuevos equipos """
    """Metodo especial constructor ---   __init__   ---"""
    def __init__(self, nombre="", no_serie='', ubicacion="", marca='', estado="", modelo='', observaciones='', barcode=''):
        self.nombre = nombre
        self.no_serie = no_serie
        self.ubicacion = ubicacion
        self.marca = marca
        self.estado = estado 
        self.modelo = modelo
        self.observaciones = observaciones 
        self.barcode = barcode
        self.db = DataBase()


    def save(self):
        register_date = self.register_time()

        sql = f"""INSERT INTO `equipos` 
        (`nombre`, `no_serie`, `ubicacion`, `marca`, `id_estado`, `modelo`, `observaciones`,  `fecha_registro`, `barcode`) 
        VALUES ('{self.nombre}', '{self.no_serie}', '{self.ubicacion}', '{self.marca}', '{self.estado}', '{self.modelo}', '{self.observaciones}', '{register_date}', '_'); """

        self.db.execute_query(sql)


    def register_time(self):    
        mex = pytz.timezone('America/Mexico_City')
        datetime_MX = datetime.now(mex)
        register_date = datetime_MX.strftime("%Y-%m-%d %H:%M:%S")

        return register_date


    def get_equipment_info(self, barcode):
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
                'barcode': f'{data[0]}',
                'nombre': f'{data[1]}', 
                'no_serie': f'{data[2]}',
                'ubicacion': f'{data[3]}',
                'marca': f'{data[4]}',
                'modelo': f'{data[5]}',
                'id_estado': f'{data[6]}',
                'observaciones': f'{data[7]}',
                'fecha_registro': f'{data[8]}',
                'barcode': f'{data[9]}',
                'estado': f'{data[11]}'
            }
            
            return equipment_info

        return data

    
    def delete_equipment(self, barcode):
        sql = f"DELETE FROM equipos WHERE barcode = '{barcode}' limit 1"
        self.db.execute_query(sql)

        return True


    def update_equipment(self):
        # considerar en agregar un campo llamado ultima_modificacion

        sql = f"""
        UPDATE `equipos`
        set nombre = '{self.nombre}',
        no_serie = '{self.no_serie}',
        ubicacion = '{self.ubicacion}',
        marca = '{self.marca}',
        id_estado = '{self.estado}',
        modelo = '{self.modelo}',
        observaciones = '{self.observaciones}'
        WHERE barcode = '{self.barcode}' limit 1;
        """

        self.db.execute_query(sql)

