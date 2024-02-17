from flask import Blueprint, jsonify, request
from src.db.service import BorrowingService

borrow_api = Blueprint('borrow_api', __name__, url_prefix='/api/borrow')

@borrow_api.route('/books/<int:user_id>')
def get_borrowed_books(user_id: int):
    books = [book.as_dict() for book in BorrowingService().get_borrowed_books_by_user(user_id)]
    return jsonify({"success": True, "result": books})


@borrow_api.route('/', methods=['POST'])
def borrow_book():
    req_body = request.json
    if not req_body:
        return jsonify({"success": False, "message": "No request body was provided."})
    
    user_id, book_id = req_body.get('user_id'), req_body.get('book_id')
    if not user_id or not book_id:
        return jsonify({"success": False, "message": f"Missing argument: {user_id=} , {book_id=}"})
    
    borrow_book = BorrowingService().borrow_book(user_id, book_id)
    if not borrow_book:
        return jsonify({"success": False, "message": f"Arguments not existing: {user_id=} , {book_id=}"})
    return jsonify({"success": True, "result": borrow_book.as_dict()})


@borrow_api.route('/return', methods=['POST'])
def return_book():
    req_body = request.json
    if not req_body:
        return jsonify({"success": False, "message": "No request body was provided."})
    
    user_id, book_id = req_body.get('user_id'), req_body.get('book_id')
    if not user_id or not book_id:
        return jsonify({"success": False, "message": f"Missing argument: {user_id=} , {book_id=}"})
    
    borrow_book = BorrowingService().return_book(user_id, book_id)
    if not borrow_book:
        return jsonify({"success": False, "message": f"Borrowed book not found: {user_id=} , {book_id=}"})
    
    return jsonify({"success": True, "result": borrow_book.as_dict()})
