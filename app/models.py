from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String(10))
    monto = db.Column(db.Float)
    descripcion = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Gasto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String(10))
    monto = db.Column(db.Float)
    descripcion = db.Column(db.String(200))
    categoria = db.Column(db.String(50))  # <- AÑADIR ESTO
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
