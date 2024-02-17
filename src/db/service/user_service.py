from src.db import db
from src.db.repository import UserRepository
from src.db.entity import User, BorrowedBook

class UserService:
    
    def __init__(self):
        self.user_repository = UserRepository()

    def get_all(self)-> list[User]:
        return User.query.all()

    def register_user(self, username: str, email: str, password: str) -> User:
        return self.user_repository.create_user(username, email, password)

    def get_user(self, email: str|None=None, username: str|None =None)-> User | None:
        if email:
            return User.query.filter_by(email=email).first()
        
        return User.query.filter_by(username=username).first()

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.user_repository.get_user_by_id(user_id)
    
    def delete_user_by_id(self, user_id: int) -> User | None:
        return self.user_repository.delete_user(user_id)

    def list_borrowed_books(self, user_id: int) -> list[BorrowedBook]:
        return BorrowedBook.query.filter_by(user_id=user_id).all()


    def delete_account(self, email: str) -> User | None:
        user = self.get_user(email=email)
        if user:
            return self.user_repository.delete_user(user.id)
        return None
        

    def change_user_info(self, user_id: int, new_email: str|None=None, new_username: str|None=None, new_password: str|None=None) -> User | None:
        update_data = {}

        if new_email is not None:
            update_data['email'] = new_email
        if new_username is not None:
            update_data['username'] = new_username
        if new_password is not None:
            update_data['password'] = new_password

        return self.user_repository.update_user(user_id, update_data)

    