import datetime
from src.db import db
from src.db.entity import BorrowedBook, Book, User

class BorrowedBookRepository:
    def borrow_book(self, user_id: int, book_id: int, borrow_date, return_date) -> BorrowedBook | None:
        book = Book.query.get(book_id)
        user = User.query.get(user_id)
        if not user or not book:
            return None
        borrowed_book = BorrowedBook(user_id=user_id, book_id=book_id, borrow_date=borrow_date, return_date=return_date)
        db.session.add(borrowed_book)
        db.session.commit()
        return borrowed_book

    def get_borrowed_books_by_user(self, user_id: int) -> list[BorrowedBook]:
        return BorrowedBook.query.filter_by(user_id=user_id).all()

    def return_book(self, borrowed_book_id: int) -> BorrowedBook | None:
        borrowed_book = BorrowedBook.query.get(borrowed_book_id)
        if borrowed_book:
            borrowed_book.return_date = datetime.date.today()
            db.session.commit()
        return borrowed_book
    
    def update_borrowed_book(self, borrowed_book_id: int, new_data: dict) -> BorrowedBook | None:
        borrowed_book = BorrowedBook.query.get(borrowed_book_id)
        if borrowed_book:
            for key, value in new_data.items():
                setattr(borrowed_book, key, value)
            db.session.commit()
        return borrowed_book

    def delete_borrowed_book(self, borrowed_book_id: int) -> BorrowedBook | None:
        borrowed_book = BorrowedBook.query.get(borrowed_book_id)
        if borrowed_book:
            db.session.delete(borrowed_book)
            db.session.commit()
        return borrowed_book