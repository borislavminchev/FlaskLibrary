from typing import Any
from flask_login import UserMixin
from src.db.database import db
import json

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column("user_id",db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def as_dict(self) -> dict[str, Any]:
        return {"id": self.id, "username": self.username, "email": self.email, "password": self.password} 