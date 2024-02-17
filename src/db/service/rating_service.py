from src.db.entity import Rating
from src.db.repository import RatingRepository, BookRepository, UserRepository

class RatingService:
    def __init__(self):
        self.rating_repository = RatingRepository()

    def rate_book(self, user_id: int, book_id: int, rating: int, review: str) -> Rating:
        return self.rating_repository.rate_book(user_id, book_id, rating, review)
    
    def get_ratings_book(self, book_id: int)-> list[Rating] | None:
        ratings = Rating.query.filter_by(book_id=book_id).all()
        if len(ratings) == 0:
             return None
        
        return ratings

    def get_ratings_user(self, user_id: int)-> list[Rating] | None:
        ratings = Rating.query.filter_by(user_id=user_id).all()
        if len(ratings) == 0:
             return None
        
        return ratings

    def get_average_rating_for_book(self, book_id: int) -> float:
        return self.rating_repository.get_average_rating_for_book(book_id)
    
    def delete_ratings(self, user_id: int, book_id: int) -> list[Rating] | None:
            return self.rating_repository.delete_rating(user_id, book_id)