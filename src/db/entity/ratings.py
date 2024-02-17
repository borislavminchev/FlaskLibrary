from typing import Any
from src.db.database import db

class Rating(db.Model):
    __tablename__ = 'ratings'

    id = db.Column("rating_id", db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.book_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    rating = db.Column(db.Integer)
    review = db.Column(db.Text)

    book = db.relationship("Book", backref="ratings")
    user = db.relationship("User", backref="ratings")

    def __init__(self, book_id, user_id, rating, review):
        self.book_id = book_id
        self.user_id = user_id
        self.rating = rating
        self.review = review

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "book_id": self.book_id,
            "user_id": self.user_id,
            "rating": self.rating,
            "review": self.review,
        }