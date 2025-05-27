from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User, Venta, Gasto

bp = Blueprint('main', __name__)

# Página principal
@bp.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("main.login"))
    return render_template("index.html")

# Registro de usuario
@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if User.query.filter_by(username=username).first():
            flash("El usuario ya existe")
            return redirect(url_for("main.register"))
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registro exitoso")
        return redirect(url_for("main.login"))
    return render_template("register.html")

# Inicio de sesión
@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session["user_id"] = user.id
            flash("Inicio de sesión exitoso")
            return redirect(url_for("main.index"))
        flash("Credenciales incorrectas")
    return render_template("login.html")

# Cerrar sesión
@bp.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("Has cerrado sesión")
    return redirect(url_for("main.login"))

# API: VENTAS
@bp.route("/api/ventas", methods=["GET", "POST"])
def api_ventas():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user_id = session["user_id"]

    if request.method == "POST":
        data = request.get_json()
        nueva_venta = Venta(
            fecha=data["fecha"],
            monto=data["monto"],
            descripcion=data["descripcion"],
            user_id=user_id
        )
        db.session.add(nueva_venta)
        db.session.commit()
        return jsonify({"message": "Venta agregada"}), 201

    ventas = Venta.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "id": v.id,
        "fecha": v.fecha,
        "monto": v.monto,
        "descripcion": v.descripcion
    } for v in ventas])

@bp.route("/api/ventas/<int:venta_id>", methods=["DELETE"])
def eliminar_venta(venta_id):
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    venta = Venta.query.get_or_404(venta_id)
    if venta.user_id != session["user_id"]:
        return jsonify({"error": "Forbidden"}), 403

    db.session.delete(venta)
    db.session.commit()
    return jsonify({"message": "Venta eliminada"}), 200

# API: GASTOS
@bp.route("/api/gastos", methods=["GET", "POST"])
def api_gastos():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user_id = session["user_id"]

    if request.method == "POST":
        data = request.get_json()
        nuevo_gasto = Gasto(
            fecha=data["fecha"],
            monto=data["monto"],
            descripcion=data["descripcion"],
            categoria=data.get("categoria", "otros"),
            user_id=user_id
        )
        db.session.add(nuevo_gasto)
        db.session.commit()
        return jsonify({"message": "Gasto agregado"}), 201

    gastos = Gasto.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "id": g.id,
        "fecha": g.fecha,
        "monto": g.monto,
        "descripcion": g.descripcion,
        "categoria": g.categoria
    } for g in gastos])

@bp.route("/api/gastos/<int:gasto_id>", methods=["DELETE"])
def eliminar_gasto(gasto_id):
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    gasto = Gasto.query.get_or_404(gasto_id)
    if gasto.user_id != session["user_id"]:
        return jsonify({"error": "Forbidden"}), 403

    db.session.delete(gasto)
    db.session.commit()
    return jsonify({"message": "Gasto eliminado"}), 200
