import os

from datetime import timedelta
from flask import Flask
from flask_login import LoginManager

from src.db import DB_URI, db
from src.login.user_login import login_manager, auth
from src.db.entity import Book, User, BorrowedBook, Rating
from src.db.service import BorrowingService
from src.controller.views.application import index
from src.controller.api import book_api, user_api, borrow_api, rating_api

from src.scheduler import scheduler

def is_borrowed(user_id, book_id):
    books = [book.id for book in BorrowingService().get_borrowed_books_by_user(user_id)]
    return book_id in books


app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = os.urandom(16)
app.jinja_env.globals.update(is_borrowed=is_borrowed)

app.register_blueprint(index)
app.register_blueprint(auth)
app.register_blueprint(book_api)
app.register_blueprint(user_api)
app.register_blueprint(borrow_api)
app.register_blueprint(rating_api)

app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
db.init_app(app)

login_manager.init_app(app)



scheduler.start()



