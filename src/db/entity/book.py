from typing import Any
from src.db.database import db
import json

class Book(db.Model):
    __tablename__ = "books"
    id = db.Column("book_id",db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    author = db.Column(db.String)
    tags = db.Column(db.String)

    def __init__(self, title, author, tags):
        self.title = title
        self.author = author
        self.tags = tags

    def as_dict(self) -> dict[str, Any]:
        return {"id": self.id, "title": self.title, "author": self.author, "tags": self.tags} 