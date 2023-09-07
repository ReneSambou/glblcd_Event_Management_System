from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

db = SQLAlchemy()

class User(db.Model):
        __tablename__ = "users"

        # fields
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
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
        event_name = db.Column(db.String(100))
        venue = db.Column(db.String(100))
        date = db.Column(db.String(100))
        time = db.Column(db.String(100))
        event_flyer =db.Column(db.String(255))
        created = db.Column(db.DateTime, server_default = sqlalchemy.func.now())