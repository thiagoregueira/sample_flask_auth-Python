from flask import Flask, request, jsonify
from models.user import User  # noqa
from database import db
import bcrypt
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)


app = Flask(__name__)
app.config["SECRET_KEY"] = "you_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://root:root@127.0.0.1:3306/flask_crud"
)


login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)

login_manager.login_view = "login"


# login/logout routes ---------------------------------------------------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data["username"]
    password = data["password"]

    if username and password:
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.checkpw(str.encode(password), str.encode(user.password)):
            login_user(user)
            return jsonify({"message": "Autenticação realizada com sucesso"}), 200

    return jsonify({"message": "Credenciais inválidas"}), 400


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout realizado com sucesso"}), 200


# user routes -----------------------------------------------------------------
# Create user -----------------------------------------------------------------
@app.route("/user", methods=["POST"])
def create_user():
    data = request.json
    username = data["username"]
    password = data["password"]

    if username and password:
        hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
        user = User(username=username, password=hashed_password, role="user")
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Usuário criado com sucesso"}), 201

    return jsonify({"message": "Dados inválidos"}), 400


# Read user -------------------------------------------------------------------
@app.route("/user/<int:id_user>", methods=["GET"])
@login_required
def read_user(id_user):
    user = User.query.get(id_user)

    if user:
        return {"username": user.username}

    return jsonify({"message": "Usuário não encontrado"}), 404


# Update user -----------------------------------------------------------------
@app.route("/user/<int:id_user>", methods=["PUT"])
@login_required
def update_user(id_user):
    data = request.json

    user = User.query.get(id_user)

    if id_user != current_user.id and current_user.role == "user":
        return (
            jsonify({"message": "Você não tem permissão para atualizar este usuário"}),
            403,
        )

    if user and data.get("password"):
        user.password = data.get("password")
        db.session.commit()
        return jsonify({"message": f"Usuário {id_user} atualizado com sucesso"}), 200

    return jsonify({"message": "Usuário não encontrado"}), 404


# Delete user -----------------------------------------------------------------
@app.route("/user/<int:id_user>", methods=["DELETE"])
@login_required
def delete_user(id_user):
    user = User.query.get(id_user)

    if current_user.role != "admin":
        return jsonify({"message": "Você não tem permissão para deletar usuários"}), 403

    if id_user == current_user.id:
        return jsonify({"message": "Você não pode deletar a si mesmo"}), 403

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"Usuário {id_user} deletado com sucesso"}), 200

    return jsonify({"message": "Usuário não encontrado"}), 404


if __name__ == "__main__":
    app.run(debug=True, port=5001)
