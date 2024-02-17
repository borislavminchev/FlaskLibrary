from src.db import db
from src.db.entity import Rating

class RatingRepository:
    def rate_book(self, user_id: int, book_id: int, rating: int, review: str)-> Rating:
        existing_rating = Rating.query.filter_by(user_id=user_id, book_id=book_id).first()

        if existing_rating:
            existing_rating.rating = rating
            existing_rating.review = review
            db.session.commit()
            return existing_rating
        else:
            new_rating = Rating(user_id=user_id, book_id=book_id, rating=rating, review=review)
            db.session.add(new_rating)
            db.session.commit()
            return new_rating

    def get_average_rating_for_book(self, book_id: int) -> float:
        avg_rating = db.session.query(db.func.avg(Rating.rating)).filter_by(book_id=book_id).scalar()
        return avg_rating if avg_rating else 0
    
    def delete_rating(self, user_id: int, book_id: int) -> list[Rating] | None:
        ratings = Rating.query.filter_by(user_id=user_id, book_id=book_id).all()
        if len(ratings) == 0:
            return None
        
        for rating in ratings:
            db.session.delete(rating)
            db.session.commit()
        return ratings