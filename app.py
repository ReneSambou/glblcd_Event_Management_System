from flask import Flask, render_template, request, flash, redirect, url_for
import database

app = Flask(__name__)
app.secret_key = '333abc'

@app.route('/')
def index():
    return render_template('signup.html')

@app.route('/submit', methods = ['POST'])
def dashboard():
    username = request.form.get('username')
    password = request.form.get('password')
    if username in database.users_database and password == database.users_database[username]:
        return render_template('dashboard.html', username=username)
    else:
        flash('Login failed. Please check your username and password.')
        return redirect('/')
    
@app.route('/logout', methods = ['POST'])
def logout():
    return redirect('/')
        
    
def bolden(func):
    def wrap():
        bold = func()
        return f'<b>{bold}<b>'
    return wrap

@app.route('/greeting/<name>/<int:age>')
def greeting(name, age):
    return f'<p>Hello, {age} year old {name} </p>'


if __name__ == "__main__":
   app.run(debug=True, host='0.0.0.0', port = 80)
