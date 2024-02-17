import datetime
from flask import Blueprint, render_template, jsonify, request, redirect, url_for, session
from flask_login import login_required, current_user
from src.db.service import UserService, BookService, BorrowingService, RatingService
from src.db.entity import User, Book, Rating
from src.recommender import BookRecommender

index = Blueprint('index', __name__)


@index.route('/')
def homescreen():
    return render_template("index.html")

@index.route('/search')
def search():
    books = session.pop('books', None)
    return render_template("search.html", books=books)


@index.route('/book/search', methods=['POST'])
def find_books_by_keyword():
    keyword = request.form.get('keyword')
    
    books = BookService().find_books(keyword)
    session['books'] = [book.as_dict() for book in books]

    return redirect(url_for('index.search'))


@index.route('/profile')
@login_required
def profile():
    recommendations = session.pop('recommendations', None)
    review = session.pop('review', None)
    
    user_books = BorrowingService().get_borrowed_books_by_user(current_user.id)
    user_rating = Rating.query.filter_by(user_id=current_user.id, book_id=review).first()
    if user_rating: print(user_rating.review)
    return render_template("profile.html", name=current_user.username, user_books=user_books, recommendations=recommendations, review=review, user_rating = user_rating)


@index.route('/book/action', methods=['POST'])
@login_required
def show_recommendations():
    book_id = request.form['id']
    if not book_id: return jsonify({
        "success": True,
        "message": "error"
    })

    if request.form.get('Like') is not None:
        simmilar_books = BookRecommender().recommend_book(int(book_id), user_id=current_user.id)
        session['recommendations'] = [b.as_dict() for b in simmilar_books]
    elif request.form.get('Review') is not None:
        session['review'] = book_id

    return redirect(url_for("index.profile"))

@index.route('/book/review', methods=['POST'])
@login_required
def give_review():
    book_id = request.form['id']
    rating = request.form['review_rating']
    content = request.form['content']
    RatingService().rate_book(current_user.id, int(book_id), int(rating), content)
    return redirect(url_for("index.profile"))    

@index.route('/book/borrow', methods=['POST'])
@login_required
def borrow_book():
    book_id = request.form['id']
    BorrowingService().borrow_book(current_user.id, int(book_id))
    return redirect(url_for("index.profile"))
