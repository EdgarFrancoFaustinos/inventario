# importa el framework flask
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from user import users, get_user


# instanciar una nueva aplicacion de flask
app = Flask(__name__)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'


# libreria para iniciar sesion
login_manager = LoginManager(app)
login_manager.login_view = "index"

@app.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('agregar_equipo'))

    if request.method == 'POST':
        email = request.form['usuario']
        password = request.form['password']

        user = get_user(email)
        if user is not None and user.check_password(password):
            login_user(user, remember=True)

        return redirect(url_for('agregar_equipo'))

    return render_template("index.html")


@app.route('/productos')
@login_required
def agregar_equipo():
    return render_template("visualizar.html")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(user_id):
    for user in users:
        if user.id == int(user_id):
            return user
    return None


# este archivo es el base
if __name__ == '__main__':
    app.run(debug=True)
    #Todo el código anterior
