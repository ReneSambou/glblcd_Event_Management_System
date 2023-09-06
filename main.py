from flask import Flask, jsonify,flash, request, render_template, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import secrets


app = Flask(__name__)

app.config['SECRET_KEY'] = '29e91ce35b1f971ad0565d93a2a3777c'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///events_management.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
db.init_app(app)


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
            return render_template('signin.html')

    @app.route('/logout')
    def logout():
        logout_user()
        flash('Logout successful!')
        return redirect(url_for('index'))


    @app.route('/signup')
    def signup():
        return render_template('signup.html')
    
    @app.route('/event')
    def event():
        return render_template('event.html')

    @app.route("/register", methods=["POST"])
    def register():
        try:
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
            
            flash("Registration successful!", "success")  
            return render_template('signin.html')
        
        except Exception as e:
            db.session.rollback() 
            flash(f"Registration failed: {str(e)}", "error")
            return redirect(url_for('signup'))

    if __name__ == "__main__":
        app.run(debug=True, host='0.0.0.0', port = 80)
