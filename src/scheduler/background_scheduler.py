import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from src.db.service import BorrowingService, UserService
from src.db.entity import BorrowedBook
from src.email import EmailService

from email.message import EmailMessage

scheduler = BackgroundScheduler()
email_service = EmailService("b2001bobby@gmail.com", "xntq sqrd ffns zple")


@scheduler.scheduled_job(trigger=CronTrigger(day="*", hour="0", minute="10"))
def return_books():
    today = datetime.date.today()
    return_books = BorrowedBook.query.filter(BorrowedBook.return_date == today).all()
    service = BorrowingService()
    for borrow_book in return_books:
        service.return_book(user_id=borrow_book.user_id, book_id=borrow_book.book_id)
        email_service.send_email("b2001bobby@gmail.com", "Return book notification", f"Dear user .... your book was returned")

@scheduler.scheduled_job(trigger=CronTrigger(day="*", hour="0", minute="10"))
def notify_users():
    today = datetime.date.today()
    return_books = BorrowedBook.query.filter(BorrowedBook.return_date > today)
    return_books = return_books.filter((BorrowedBook.return_date - today).days < 1).all()
    for borrow_book in return_books:
       print(f"Sending email: {borrow_book.user_id}, {borrow_book.book_id=}")
       user = UserService().get_user_by_id(borrow_book.user_id)
       if not user: print("No user found")
       else:
        email_service.send_email("b2001bobby@gmail.com", "Return book notification", f"Dear user {user.username} please return your book")

