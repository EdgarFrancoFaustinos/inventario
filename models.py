# se importa el modulo pymysql que nos ayuda para hacer conexiones a la db en python
import pymysql

class DataBase:
    """ Esta clase establece una nueva conexion con nuestra base de datos"""

    def connect(self):
        self.connection = pymysql.connect(
            host='localhost',
            user= 'root',
            passwd='1149',
            db='sistema'
            )

        self.cursor = self.connection.cursor()


    def execute_query(self, sql):
        """ Esta funcion se encarga de ejecutar las sentencias SQL que recibe como parametro
            y retorna el resultado de la consulta
        """
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            data = self.cursor.fetchall()
        except Exception as e:
            self.connect()
            self.cursor.execute(sql)
            self.connection.commit()
            data = self.cursor.fetchall()
        finally:
            self.connection.close()

        return data
