# importa el framework flask asi como sus metodos
from flask import Flask, render_template, request, redirect, url_for, flash, session

#libreria usada para poner seguridad en login
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

#importamos nuestro archivo user que contiene nuestra clase usuario
from user import User

#importamos la clase de equipo
from equipment import Equipment

# creamos una instancia de User para usar sus metodos despues
user_class = User()

#instanciamos la clase para usar metodos y atributos
equipment_class = Equipment()

# creamos nuestra aplicacion de flask
app = Flask(__name__)

# la SECRET_KEY nos ayuda a cifrar las cookies en el navegador y hacer el login seguro
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'


# creamos instancia de la libreria LoginManager
login_manager = LoginManager(app)

# si protegemos una vista, y alguien trata de acceder lo retorna a la funcion index para que se loguee
login_manager.login_view = "login"


@app.route('/', methods=['GET', 'POST'])
def login():
    """ Esta funcion se encarga de recibir el username y password para el inicio de sesion """

    if current_user.is_authenticated:
        return redirect(url_for('inicio'))

    if request.method == 'POST':
        email = request.form['usuario']
        password = request.form['password']

        user = user_class.get_user(email)
        if user is not None and user.check_password(password):
            login_user(user, remember=True)
        else:
            flash('Usuario o contraseña incorrectos')

        return redirect(url_for('inicio'))

    return render_template("login.html")


@app.route('/inicio')
@login_required
def inicio():
    """ si existe una sesion lo mandara a esta funcion, caso contrario lo retorna al index """

    return render_template("inicio.html")


@app.route('/agregar', methods=['GET', 'POST'])
@login_required
def agregar():
    """ Se encarga de recibir los datos enviados a tráves del form y los guarda en la db """

    if request.method == 'POST':
        nombre = request.form['nombre']
        serie = request.form['no_serie']
        ubicacion = request.form['ubicacion']
        marca = request.form['marca']
        estado = request.form['estado']
        resguardo = request.form['resguardatario']
        modelo = request.form['modelo']
        codigo = request.form['barcode']
        observaciones = request.form['observaciones']
        # print(name, serie, ubicacion, marca, estado, modelo, observaciones)
        # print("*"*50)

        newEquipment = Equipment(nombre, serie, ubicacion, marca, estado, resguardo ,modelo,observaciones, codigo)
        newEquipment.save()

        flash('Equipo guardado')

        return redirect(url_for('inicio'))

    return render_template("agregar.html")


@app.route('/actualizar', methods=['GET', 'POST'])
@login_required
def actualizar():
    """ Se encarga de obtener los datos a actualizar, en caso de no recibir algun cambio ese dato seguira siendo el mismo """

    if request.method == 'POST':
        equipment_id = request.form['equipment_id']
        nombre= request.form['nombre']
        serie = request.form['no_serie']
        ubicacion = request.form['ubicacion']
        marca = request.form['marca']
        estado = request.form['estado']
        resguardo = request.form['resguardatario']
        modelo = request.form['modelo']
        observaciones = request.form['observaciones']
        barcode = request.form['barcode']

        updateEquipment = Equipment(nombre, serie, ubicacion, marca, estado, resguardo,modelo, observaciones, barcode)
        updateEquipment.update_equipment(equipment_id)

        flash('Equipo actualizado correctamente')
        return redirect(url_for('inicio'))


    if not 'data' in session:
        data = {}
    else:
        data = session.get('data')
        session.pop('data', None)

    context = {
        'data': data
    }

    return render_template('actualizar.html', **context)


@app.route('/eliminar', methods=['GET', 'POST'])
@login_required
def eliminar():
    """ Elimina algun equipo de la db, manda como parametro el barcode del equipo a eliminar"""

    if request.method == 'POST':
        barcode = request.form['barcode']
        equipment_class.delete_equipment(barcode)

        flash('Equipo eliminado correctamente')

        return redirect(url_for('inicio'))


    if not 'data' in session:
        data = {}
    else:
        data = session.get('data')
        session.pop('data', None)

    context = {
        'data': data
    }

    return render_template('eliminar.html', **context)


@app.route('/visualizar', methods=['GET', 'POST'])
@login_required
def visualizar():
    """ Obtiene todos los equipos de nuestra db, en caso de usar un filtro manda los parametros para filtrar """

    if request.method == 'POST':
        filtro = request.form['filtro']
        filtro_elegido = request.form['filtro-elegido']

        if not equipment_class.check_if_filter_keyword_exist(filtro):
            flash('Por favor elige un filtro correcto')
            return redirect(url_for('visualizar'))

        equipments = equipment_class.get_all_the_equipments(filtro, filtro_elegido)

        if not equipments:
            flash("No se encontraron resultados, intenta nuevamente")
            equipments = equipment_class.get_all_the_equipments()
    else:
        equipments = equipment_class.get_all_the_equipments()

    context = {
        'equipments': equipments
    }

    return render_template("visualizar.html", **context)


@app.route('/buscar_equipo_por_codigo/<nombre_funcion>', methods=['GET', 'POST'])
@login_required
def buscar(nombre_funcion):
    """ Función auxiliar para buscar un equipo usando el barcode, nos sirve la funcion eliminar y actualizar """

    if request.method == 'POST':
        barcode = request.form['barcode']

        data = equipment_class.get_equipment_info(barcode)

        if data:
            session['data'] = data
            return redirect(url_for(nombre_funcion))

    flash('El equipo no existe')
    return redirect(url_for(nombre_funcion))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@login_manager.user_loader
def load_user(user_id):
    """ si detecta que hay inición iniciada valida que sea del usuario que la consulta """

    user = user_class.get_user_by_id(int(user_id))
    return user


# este archivo es el base
if __name__ == '__main__':
    app.run(debug=True)
    #Todo el código anterior




#Este es el archivo principal que necesita flask, donde estan las rutas del sistema web.
