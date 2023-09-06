from flask import Flask, jsonify,flash, request, render_template, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import secrets
import db_py

from db_py import User


app = Flask(__name__)

app.config['SECRET_KEY'] = '29e91ce35b1f971ad0565d93a2a3777c'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///events_management.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        login_user(user)
        flash('Login successful!')
        return redirect(url_for('index'))
    else:
        flash('Login failed. Please check your email and password.')
        return redirect(url_for('signin'))

@app.route('/logout')
def logout():
    logout_user()
    flash('Logout successful!')
    return redirect(url_for('index'))


@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify(response={"error": "Email already exists."}), 400

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

    new_user = User(name=name, email=email, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()
    return jsonify(response={"success": "Registration successful."})


if __name__ == "__main__":
   app.run(debug=True, host='0.0.0.0', port = 80)
