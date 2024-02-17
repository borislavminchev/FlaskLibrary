import datetime
from src.db.repository import BorrowedBookRepository
from src.db.entity import BorrowedBook, Book


class BorrowingService:
    def __init__(self):
        self.borrowed_book_repository = BorrowedBookRepository()
        
    def get_borrowed_books_by_user(self, user_id: int)->list[Book]:
        today = datetime.date.today()
        borrowed_books = BorrowedBook.query.filter_by(user_id=user_id).filter(BorrowedBook.return_date >= today).all()
        return [borrowed_book.book for borrowed_book in borrowed_books]

    def borrow_book(self, user_id: int, book_id: int) -> BorrowedBook | None:
        today = datetime.date.today()
        return_date= datetime.date(today.year, today.month+1, today.day)
        return self.borrowed_book_repository.borrow_book(user_id, book_id, today, return_date)

    def return_book(self, user_id: int, book_id: int) -> BorrowedBook | None:
       borrowed_book = BorrowedBook.query.filter_by(user_id=user_id, book_id=book_id).first()
       if not borrowed_book:
           return None
       return self.borrowed_book_repository.return_book(borrowed_book.transaction_id)
    
    def update_borrowed_book(self, borrowed_book_id: int, new_data: dict) -> BorrowedBook | None:
        return self.borrowed_book_repository.update_borrowed_book(borrowed_book_id, new_data)

    def delete_borrowed_book(self, borrowed_book_id: int) -> BorrowedBook | None:
        return self.borrowed_book_repository.delete_borrowed_book(borrowed_book_id)

