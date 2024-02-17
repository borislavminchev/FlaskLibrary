from src.db import db
from src.db.entity import User

class UserRepository:
    def create_user(self, username: str, email: str, password: str) -> User:
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return user

    def get_user_by_id(self, user_id: int) -> User | None:
        return User.query.get(user_id)

    def get_user_by_username(self, username: str) -> User | None:
        return User.query.filter_by(username=username).first()
    
    def update_user(self, user_id: int, new_data: dict) -> User | None:
        user = User.query.get(user_id)
        if user:
            for key, value in new_data.items():
                setattr(user, key, value)
            db.session.commit()
        return user

    def delete_user(self, user_id: int) -> User | None:
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
        return user