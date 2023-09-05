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


with app.app_context():
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

    # HTTP POST - Create Record
    @app.route("/register", methods=["POST"])
    def register():
        # get user information from postman post
        name = request.form.get("name"),
        email = request.form.get("email"),
        password = request.form.get("password")

        # Check if the email already exists in the database
        existing_user = User.query.filter_by(email=request.form.get("email")).first()

        if existing_user:
            return jsonify(response={"error": "Email already exists."}), 400

        # # Check if user email is already present in the database.
        # result = db.session.execute(db.select(User).where(User.email == request.form.get('email')))
        # user = result.scalar()
        #
        # # User already exists?
        # if user:
        #     return "User already exists!"

        # hash password for security purpose
        hash_and_salted_password = generate_password_hash(
            password,
            method='pbkdf2:sha256',
            salt_length=8
        )

        # create user record using the post information with the User class model schema
        new_user = User(
            name=name[0],
            email=email[0],
            password=hash_and_salted_password
        )

        # add the user record to the user database
        db.session.add(new_user)

        # commit the changes
        db.session.commit()
        return jsonify(response={"success": "Successfully added the new cafe."})

    # GET: all users in json format
    @app.route('/all')
    def all_users():
        users = db.session.query(User).all()
        return jsonify(users=[user.to_dict() for user in users])


    if __name__ == "__main__":
        app.run(debug=True, port=5001)
