from typing import Any
from src.db import db
from src.db.entity import Book, BorrowedBook

from .rating_repository import RatingRepository

class BookRepository:

    def is_book_available(self, book_id) -> bool:
        borrowed_book = BorrowedBook.query.filter_by(book_id=book_id, return_date=None).first()
        return not borrowed_book  # Book is available if there are no active borrow records

    def get_book_details(self, book_id: int) -> dict[str, Any] | None:
        book = Book.query.get(book_id)
        if book:
            rating_repository = RatingRepository()
            return {
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'tags': book.tags,
                'available': self.is_book_available(book.id),
                'average_rating': rating_repository.get_average_rating_for_book(book.id),
            }
        return None

    def list_all_books(self)->list[Book]:
        return Book.query.all()

    def get_book_by_id(self, book_id: int) -> Book | None:
        return Book.query.get(book_id)

    def add_new_book(self, title: str, author: str, tags: str) -> Book:
        book = Book(title=title, author=author, tags=tags)
        db.session.add(book)
        db.session.commit()
        return book
    
    def update_book(self, book_id: int, new_data: dict) -> Book | None:
        book = Book.query.get(book_id)
        if book:
            for key, value in new_data.items():
                setattr(book, key, value)
            db.session.commit()
        return book

    def delete_book(self, book_id: int) -> Book | None:
        book = Book.query.get(book_id)
        if book:
            db.session.delete(book)
            db.session.commit()
        return book