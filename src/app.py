"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap #manejar errores y mostar todo mis GET en el explorador
from admin import setup_admin
from models import db, User, Drink #base de datos
#from models import Person

# conexion a base de datos
app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app) #configura el panel de administracion mediante la extension de flask admin,Flask-AdminLTE, Flask-AdminPanel, entre otras.EN este caso se hace en admin.py


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generar un mapa del sitio con todos sus puntos finales
# me permite visualizar en el explorador los Get
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/users', methods=['GET'])
def handle_hello():
    #como estamos heredando podemos hacer esto
    users = User.query.all() #hace una consulta a la bd y devuelve una lista con todos los registro y cada reltado sera un objeto de la calse user que corresponde a un usuario,

    return jsonify([user.serialize() for user in users ]), 200 # el user.serialize() es una funcion flecha , puede ser person.serialixze

@app.route('/drink', methods = ['POST', 'GET'])
def add_drink():
    if request.method == "GET":
        drinks = Drink.query.all()
        return jsonify ([bebida.serialize() for bebida in drinks]) #el serialize es porque necesitamos devolver un diccionario y no objeto
        


    body = request.json # para recuperar body o obtener la informacion del body

# para capturar lo que se escribe en el body
    name = body.get("name")
    precio = body.get("precio")
   
    if name != None and precio != None : 
        new_drink = Drink(name = name, precio = precio) # se le pasa el constructor
        db.session.add(new_drink)
        db.session.commit()
        return jsonify(new_drink.serialize()), 200
    
    return jsonify ({"msg": "Error missing keys"}),400

# this only runs if `$ python src/app.py` is executed
# esto solo se ejecuta si se ejecuta `$ python src/app.py`
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
