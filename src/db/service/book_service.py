from src.db.entity import Book
from src.db.repository import BookRepository, BorrowedBookRepository

class BookService:
    
    def __init__(self):
        self.book_repository = BookRepository()
        self.borrowing_service = BorrowedBookRepository()

    def list_all_books(self)-> list[Book]:
        return self.book_repository.list_all_books()

    def get_book_by_id(self, book_id) -> Book | None:
        return self.book_repository.get_book_by_id(book_id)
    
    def find_books(self, keyword: str|None, num_results=10) -> list[Book]:
        all_books = self.book_repository.list_all_books()

        if not keyword:
            return all_books
        
        word = keyword.lower()

        matching_books = [
            book for book in all_books
            if word in book.title.lower() or word in book.author.lower()
        ]

        return matching_books[:num_results]
    

    def get_all_books(self, user_id=int|None, tags: list[str] = []) -> list[Book]:
        if not user_id:
            books = self.book_repository.list_all_books()
        else:
            borrowed_books = self.borrowing_service.get_borrowed_books_by_user(int(user_id))
            borrowed_book_ids = [borrowed_book.book_id for borrowed_book in borrowed_books]

            books = [book for book in self.book_repository.list_all_books() if book.id in borrowed_book_ids]
        

        if tags:
            books = [book for book in books if any(tag in book.tags.split('#') for tag in tags)]

        return books

    def add_new_book(self, title: str, author: str, tags: str) -> Book:
        return self.book_repository.add_new_book(title, author, tags)

    def update_book(self, book_id: int, new_data: dict) -> Book | None:
        return self.book_repository.update_book(book_id, new_data)

    def delete_book(self, book_id: int) -> Book | None:
        return self.book_repository.delete_book(book_id)

    def get_book_details(self, book_id):
        return self.book_repository.get_book_details(book_id)

   
    


