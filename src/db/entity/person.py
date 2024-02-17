from src.db.database import db
import json

class Person(db.Model):
    __tablename__ = "person"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    address = db.Column(db.String)
    email = db.Column(db.String)
    phone = db.Column(db.String)
    wallet = db.Column(db.String)

    def __repr__(self):
        return f"<Person {self.id=}, {self.name=}, {self.email=}, {self.wallet=}>"