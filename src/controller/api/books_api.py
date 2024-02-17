from flask import Blueprint, jsonify, request

from src.db.service import BookService

book_api = Blueprint("book_api", __name__, url_prefix='/api/books')


@book_api.route('/', methods=['GET'])
def all_books():
    books = [book.as_dict() for book in BookService().list_all_books()]
    return jsonify({"success": True, "result": books})


@book_api.route('/<int:book_id>', methods=['GET'])
def get_book(book_id: int):
    book = BookService().get_book_by_id(book_id)
    if not book:
        return jsonify({"success": False, "message": f"Book with id: {book_id} was not found."})
    return jsonify({"success": True, "result": book.as_dict()})


@book_api.route('/search', methods=['POST'])
def search_book():
    req_body = request.json
    if not req_body:
        return jsonify({"success": False, "message": "No request body was provided."})
    
    keyword, size = req_body.get('keyword'), req_body.get('size', 5)
    if not keyword:
        return jsonify({"success": False, "message": "Missing keyword argument."})
    
    books = [book.as_dict() for book in BookService().find_books(keyword=keyword, num_results=size)]
    return jsonify({"success": True, "result": books})


@book_api.route('/filtered', methods=['POST'])
def get_books_filtered():
    req_body = request.json
    if not req_body:
        return jsonify({"success": False, "message": "No request body was provided."})
    
    user_id, tags = req_body.get('user_id'), req_body.get('tags', [])
    books = [book.as_dict() for book in BookService().get_all_books(user_id=user_id, tags=tags)]
    return jsonify({"success": True, "result": books})