from flask import Blueprint, jsonify, request, render_template
from userapi.src import db
from userapi.src.models import User

bp = Blueprint("api", __name__, template_folder="templates")


@bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@bp.route("/api", methods=["GET"])
def api_info():
    return jsonify({"message": "UserAPI v1.0", "status": "running"})


@bp.route("/health", methods=["GET"])
def health():
    try:
        db.session.execute(db.text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    status = "ok" if db_status == "healthy" else "degraded"
    return jsonify({"status": status, "database": db_status}), (200 if status == "ok" else 503)


@bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    errors = User.validate(data)
    if errors:
        return jsonify({"errors": errors}), 422

    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username already exists"}), 409
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already exists"}), 409

    user = User(
        username=data["username"],
        email=data["email"],
        firstname=data.get("firstname"),
        lastname=data.get("lastname"),
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@bp.route("/users", methods=["GET"])
def get_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return jsonify([u.to_dict() for u in users])


@bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict())


@bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    if "username" in data and data["username"] != user.username:
        if User.query.filter_by(username=data["username"]).first():
            return jsonify({"error": "Username already exists"}), 409
        user.username = data["username"]

    if "email" in data and data["email"] != user.email:
        if "@" not in data["email"]:
            return jsonify({"error": "Invalid email"}), 422
        if User.query.filter_by(email=data["email"]).first():
            return jsonify({"error": "Email already exists"}), 409
        user.email = data["email"]

    user.firstname = data.get("firstname", user.firstname)
    user.lastname = data.get("lastname", user.lastname)

    db.session.commit()
    return jsonify(user.to_dict())


@bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"User {user_id} deleted successfully"})
