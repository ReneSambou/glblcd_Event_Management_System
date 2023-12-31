from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

db = SQLAlchemy()

class User(UserMixin, db.Model):
        __tablename__ = "User"

        # fields
        is_active = db.Column(db.Boolean, default=True)
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100))
        email = db.Column(db.String(100), unique=True)
        password = db.Column(db.String(100))

        def to_dict(self):
            """
                representing the user record in dictionary format
                :return:
            """
            dictionary = dict()
            for column in self.__table__.columns:
                dictionary[column.name] = getattr(self, column.name)
            return dictionary
        
class Event(db.Model):
        __tablename__ = "Event"

        id = db.Column(db.Integer, primary_key=True)
        #user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
        event_name = db.Column(db.String(100))
        venue = db.Column(db.String(100))
        date = db.Column(db.String(100))
        time = db.Column(db.String(100))
        created = db.Column(db.DateTime, server_default = sqlalchemy.func.now())