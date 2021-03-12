# importa el framework flask
from flask import Flask, render_template

# instanciar una nueva aplicacion de flask
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/agregar')
def agregar_equipo():
    return "Hola mundo" 


# este archivo es el base
if __name__ == '__main__':
    app.run(debug=True)
    #Todo el código anterior 