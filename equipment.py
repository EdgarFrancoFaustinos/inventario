from models import DataBase

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
        sql = f"""INSERT INTO `inventarios`.`equipos` 
        (`nombre`, `no_serie`, `ubicacion`, `marca`, `id_estado`, `modelo`, `observaciones`,  `fecha_registro`, `barcode`) 
        VALUES ('{self.nombre}', '{self.no_serie}', '{self.ubicacion}', '{self.marca}', '{self.estado}', '{self.modelo}', '{self.observaciones}', '2021-03-18 12:45:34', '_');"""

        self.db.execute_query(sql)   
