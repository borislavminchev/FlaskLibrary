from flask import Blueprint, jsonify, request

from src.db.service import RatingService

rating_api = Blueprint('rating_api', __name__, root_path='/api/ratings')


@rating_api.route('/book/<int:id>')
def get_book_raings(id: int):
    ratings = RatingService().get_ratings_book(id)
    if not ratings:
        return jsonify({"success": False, "message": f"No ratings were found: {id=}"})
    
    return jsonify({
        "success": True,
        "result": [rating.as_dict() for rating in ratings]
        })


@rating_api.route('/user/<int:id>')
def get_user_raings(id: int):
    ratings = RatingService().get_ratings_user(id)
    if not ratings:
        return jsonify({"success": False, "message": f"No ratings were found: {id=}"})
    
    return jsonify({
        "success": True,
        "result": [rating.as_dict() for rating in ratings]
        })


@rating_api.route('/', methods=['POST'])
def rate_book():
    req_body = request.json
    if not req_body:
        return jsonify({"success": False, "message": "Request body not provided"})
    
    user_id, book_id = req_body.get('user_id'), req_body.get('book_id')
    rating, review = req_body.get('rating'), req_body.get('review')
    if not user_id or not book_id or not rating or not review:
        return jsonify({"success": False, "message": f"Data not provided: {user_id=}, {book_id=}, {rating=}, {review=}"})
    
    book_rating = RatingService().rate_book(user_id=user_id, book_id=book_id, rating=rating, review=review)
    return jsonify({"success": True, "result": book_rating.as_dict()})


@rating_api.route("/delete", methods=["POST"])
def delete_rating():
    req_body = request.json
    if not req_body:
        return jsonify({"success": False, "message": "Request body not provided"})
    user_id, book_id = req_body.get('user_id'), req_body.get('book_id')
    if not user_id or not book_id:
        return jsonify({"success": False, "message": f"Data not provided: {user_id=}, {book_id=}"})
    
    ratings = RatingService().delete_ratings(user_id=user_id, book_id=book_id)
    if not ratings:
        return jsonify({"success": False, "message": "No ratings were found"})
    
    return jsonify({
        "success": True,
        "result": [rating.as_dict() for rating in ratings]
        }) 