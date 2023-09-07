from flask import Flask, jsonify,flash, request, render_template, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import secrets
from models import db, Event, User


app = Flask(__name__)

app.config['SECRET_KEY'] = '29e91ce35b1f971ad0565d93a2a3777c'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///events_management.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id);


with app.app_context():
    db.create_all()  

    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.html')
    
    @app.route('/login', methods=['POST'])
    def login():
        return render_template('signin.html')

    @app.route('/event', methods=['POST'])
    def event():
        
        email = request.form.get('email')
        password = request.form.get('password')
        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()
        name = request.form.get('name')

        if user and check_password_hash(user.password, password):
            login_user(user)
            return render_template('event.html', name = name)
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
    
    @app.route('/event_form', methods = ["POST"])
    def event_form():
        return render_template('add_events.html')
    
    @app.route('/add_events', methods = ["POST"])
    def add_events():
        events_name = request.form.get("name")
        existing_event = db.session.query(Event).where(Event.event_name == events_name).first()

        if existing_event:                                                                                                                                                                                                                               
            flash('Event already exists.')
            return render_template('add_events.html')
        
        venue = request.form.get("venue")
        date = request.form.get("date")
        time = request.form.get("time")
        event_flyer = request.form.get("flyer")
        file = request.files['flyer']
        
        new_event= Event(
            event_name = events_name,
            venue = venue,
            date = date,
            time = time,
            event_flyer = event_flyer,
            event_flyer_content = file.read()
        )

        db.session.add(new_event)
        db.session.commit()

        all_events = db.session.query(Event).all()
        return render_template('event.html', all_event = all_events)
    
    
    @app.route("/events", methods = ['GET', 'POST'])
    def add():
        all_events = db.session.query(Event).all()
        return render_template('event.html', all_event = all_events)

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
