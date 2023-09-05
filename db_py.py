from flask import Flask, jsonify, request
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

from datetime import datetime
import secrets


# initialize flask app
app = Flask(__name__)
secret_key = secrets.token_hex(16)
app.config['SECRET_KEY'] = secret_key


# CONNECT TO DB: DB_URI will be used when upgrading sqlite to postgres in production
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///events_management.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# database configuration
db = SQLAlchemy(app)
# db.init_app(app)


with app.app_context():
    class User(db.Model):
        __tablename__ = "users"

        # fields
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100))
        email = db.Column(db.String(100), unique=True)
        password = db.Column(db.String(100))

        def to_dict(self):
            dictionary = dict()
            for column in self.__table__.columns:
                dictionary[column.name] = getattr(self, column.name)
            return dictionary


        # # CONFIGURE TABLES
        # class Event(db.Model):
        #     __tablename__ = "events"
        #     id = db.Column(db.Integer, primary_key=True)
        #     # Create Foreign Key, "users.id". To reference user table with the event id.
        #     event_id = db.Column(db.Integer, db.ForeignKey("users.id"))
        #     title = db.Column(db.String(250), unique=True, nullable=False)
        #     date = db.Column(db.String(250), nullable=False)
        #     description = db.Column(db.Text, nullable=False)
        #
        #
        # # CONFIGURE TABLES
        # class Booking(db.Model):
        #     __tablename__ = "bookings"
        #     id = db.Column(db.Integer, primary_key=True)
        #     # Create Foreign Key, "users.id". To reference user table with the booking id.
        #     user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
        #     # Create Foreign Key, "users.id". To reference user table with the event id.
        #     event_id = db.Column(db.Integer, db.ForeignKey("events.id"))
        #     date_time = db.Column(db.DateTime, default=datetime.utcnow)


    # HTTP POST - Create Record
    @app.route("/register", methods=["POST"])
    def register():
        new_user = User(
            name=request.form.get("name"),
            email=request.form.get("email"),
            password=request.form.get("password")
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify(response={"success": "Successfully added the new cafe."})


    @app.route('/all')
    def all_users():
        users = db.session.query(User).all()
        return jsonify(users=[user.to_dict() for user in users])


    if __name__ == "__main__":
        app.run(debug=True, port=5001)
