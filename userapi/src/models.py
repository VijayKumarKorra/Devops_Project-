from datetime import datetime, timezone
from userapi.src import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    firstname = db.Column(db.String(50), nullable=True)
    lastname = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    @staticmethod
    def validate(data):
        errors = []
        if not data.get("username"):
            errors.append("username is required")
        if not data.get("email"):
            errors.append("email is required")
        elif "@" not in data["email"]:
            errors.append("email is invalid")
        return errors

    def __repr__(self):
        return f"<User {self.username}>"
