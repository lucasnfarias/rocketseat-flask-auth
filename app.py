from flask import Flask, request, jsonify
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from models.user import User
from database import db

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)

login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)

@app.route('/login', methods=["POST"])
def login():
  data = request.json
  username = data.get("username")
  password = data.get("password")

  if username and password:
    user = User.query.filter_by(username=username).first()

    if user and user.password == password:
      login_user(user)
      return jsonify({"message": "Successfully authenticated."})

  return jsonify({"message": "Invalid credentials."}), 401

@app.route('/logout', methods=["GET"])
@login_required
def logout():
  logout_user()

  return jsonify({"message": "Successful logout."})

@app.route('/user', methods=["POST"])
def create_user():
  data = request.json
  username = data.get("username")
  password = data.get("password")

  if username and password:
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User successfully created."})

  return jsonify({"message": "Invalid fields."}), 400

@app.route('/user/<int:user_id>', methods=["GET"])
@login_required
def read_user(user_id):
  user = User.query.get(user_id)

  if user:
      return {"username": user.username}

  return jsonify({"message": "User not found."}), 404

@app.route('/user/<int:user_id>', methods=["PUT"])
def update_user(user_id):
  data = request.json

  if not data.get("password"):
    return jsonify({"message": "Password field not found."}), 400

  user = User.query.get(user_id)

  if user:
      user.password = data.get("password")
      db.session.commit()

      return jsonify({"message": f"User {user_id} updated successfully."})

  return jsonify({"message": "User not found."}), 404

@app.route('/user/<int:user_id>', methods=["DELETE"])
@login_required
def delete_user(user_id):
  if user_id == current_user.id:
    return jsonify({"message": f"Cannot delete current authenticated user: {user_id}"}), 400

  user = User.query.get(user_id)

  if user:
      db.session.delete(user)
      db.session.commit()

      return jsonify({"message": f"User {user_id} deleted successfully."})

  return jsonify({"message": "User not found."}), 404

@app.route("/hello-world", methods=["GET"])
def hello_world():
    return "hello world!"

if __name__ == '__main__':
      app.run(debug=True)
