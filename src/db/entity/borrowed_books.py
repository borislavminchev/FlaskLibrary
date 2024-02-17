from typing import Any
from src.db.database import db

class BorrowedBook(db.Model):
    __tablename__ = 'borrowed_books'

    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    borrow_date = db.Column(db.Date)
    return_date = db.Column(db.Date)

    book = db.relationship('Book', backref='borrowed_books')
    user = db.relationship('User', backref='borrowed_books')

    def __init__(self, book_id, user_id, borrow_date, return_date):
        self.book_id = book_id
        self.user_id = user_id
        self.borrow_date = borrow_date
        self.return_date = return_date

    def as_dict(self) -> dict[str, Any]:
        return {
            "book_id": self.book_id,
            "user_id": self.user_id,
            "borrow_date": self.borrow_date,
            "return_date": self.return_date
        }