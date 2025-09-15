from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import os

app = Flask(__name__)

# Подключение к Postgres через переменную окружения
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL", "postgresql://authuser:authpass@db:5432/authdb"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY", "super-secret-key")

db = SQLAlchemy(app)
jwt = JWTManager(app)


# ===== Модель пользователя =====
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# ===== Регистрация =====
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Username and password required"}), 400

    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "User exists"}), 400

    user = User(username=data["username"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Registered"}), 201


# ===== Логин =====
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Username and password required"}), 400

    user = User.query.filter_by(username=data["username"]).first()

    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(
        identity=user.id, expires_delta=datetime.timedelta(hours=1)
    )
    resp = make_response(jsonify({"message": "Logged in"}))
    # ⚡️ SameSite=None + secure=False для работы с фронтом на другом порту
    resp.set_cookie("token", token, httponly=True, samesite="None", secure=False)
    return resp


# ===== Тестовый эндпоинт =====
@app.route("/me", methods=["GET"])
def me():
    return jsonify({"message": "You are authorized"}), 200


# ===== Запуск =====
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # создаст таблицы в Postgres при старте
    app.run(host="0.0.0.0", port=5000)

