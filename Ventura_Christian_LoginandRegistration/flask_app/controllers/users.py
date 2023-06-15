from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.user import User

@app.route('/') #login page
def index():
    return render_template('login.html')

@app.route('/register', methods=['POST']) #register form submission
def register():
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'username': request.form['username'],
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'], 
        'password': pw_hash
    }
    user_id = User.createUser(data)
    print(str(user_id) + " was created.")
    print(data)
    session['user_id'] = user_id
    return redirect('/success')

@app.route('/login', methods=['POST']) # login form submission
def login():
    data = {
        'email': request.form['email']
    }
    user = User.login(data)
    print("User:", user)   #debugging
    if user is None:
        flash("Invalid email/password.")
        return redirect('/')
    print("User password:", user.password)  #debugging
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid email/password.")
        return redirect('/')
    session['user_id'] = user.id
    session['first_name'] = user.first_name
    session['logged_in'] = True
    print("Session:", session)  #debugging
    return redirect('/success')

@app.route('/success') #success page
def success():
    if 'user_id' not in session:
        flash("Please log in.")
        return redirect('/')
    user = User.getUserById({'id': session['user_id']})
    return render_template('page.html' , user = user)

@app.route('/logout') #logout
def logout():
    session.clear()
    return redirect('/')

