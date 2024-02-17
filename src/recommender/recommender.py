from typing import List
from src.db.entity import Book
from src.db.repository import BookRepository
from src.db.service import BorrowingService

class BookRecommender:
    def __init__(self):
        self.book_repository = BookRepository()
        self.borrowing_service = BorrowingService()

    def recommend_book(self, book_id: int, user_id: int|None = None, num_recommendations: int = 5) -> list[Book]:
        book = self.book_repository.get_book_by_id(book_id)

        user_owned_books = []
        if user_id is not None:
            user_owned_books = self.borrowing_service.get_borrowed_books_by_user(user_id)

        user_owned_book_ids = set(book.id for book in user_owned_books)

        if not book:
            return []

        book_tags = self.__extract_tags(book.tags)

        all_books = self.book_repository.list_all_books()

        available_books = [book for book in all_books if book.id not in user_owned_book_ids]

        similarity_scores = [
            (other_book, self.calculate_similarity(book_tags, self.__extract_tags(other_book.tags)))
            for other_book in available_books
            if other_book.id != book.id
        ]

        sorted_recommendations = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

        return [recommendation[0] for recommendation in sorted_recommendations[:num_recommendations]]

    @staticmethod
    def __extract_tags(tag_str: str)->set[str]:
        return set(tag for tag in tag_str.split('#') if tag.strip())

    @staticmethod
    def calculate_similarity(set1: set[str], set2: set[str]) -> float:
        # Simple Jaccard similarity calculation
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union if union != 0 else 0
