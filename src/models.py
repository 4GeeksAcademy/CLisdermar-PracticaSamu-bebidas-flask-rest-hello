from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() #crea una instancia de en SQLAlchemy flask.Configura la conexion con la base de datos para que flask inreractue con los datos

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

# se utiliza para obtener en mejor representacion los datos y Debuguear mejor porque nos inicaria donde esta exactamente el error 
# el % es un formateo de texto,y el %r genera una representacion que sera una cadena de texto*/
    def __repr__(self):
        return '<User %r>' % self.username

    # Obtengo el valor de mi objeto , aqui se tiene (llave, valor)
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
class Drink(db.Model):
        __tablename__= "drink"
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(380),nullable = False)
        precio = db.Column(db.Float,nullable = False)

        def __init__(self, name,precio):
             self.name = name
             self.precio = precio
             pass

        def __repr__(self):
            return'<Drink %r>' % self.name
        
        def serialize(self):
            return{
                "id":self.id,
                "name" : self.name,
                 "precio" : self.precio
            }