from flask_app import app, render_template, redirect, request, bcrypt, session, flash
from flask_app.models.user import User

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/register', methods = ['POST'])
def reg():
  #checking to see if the form is printing in the terminal.
  print(request.form)
  #if the user fills out the form wrong return them to the home page.
  if not User.validate_user(request.form):
    return redirect('/')
  # hashing password.
  pw_hash = bcrypt.generate_password_hash(request.form['password'])
  print(pw_hash)
  #dictionary of the users info.
  data = {
    'first_name':request.form['first_name'],
    'last_name':request.form['last_name'],
    'email':request.form['email'],
    'password':pw_hash
  }
  #saving users info to the database
  user_id= User.save(data)
  session['user_id'] = user_id
  session['first_name'] = data['first_name']
    #if its valid return to the show page.
  return redirect('/show')

@app.route('/login', methods=['POST'])
def login():
    # Checking to see if the user exist
    data={
      "email" : request.form["email"]
    }
    user_in_db = User.get_email(data)
    # if the users email doesnt exist redirect to the home page.
    if not user_in_db:
        flash("Invalid email or password")
        print("Invalid email or password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if the password doesnt match redirect to the home page.
        flash("Invalid email or password")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name
    print(user_in_db.id)
    return redirect("/show")

@app.route('/show')
def show():
  if 'user_id' not in session:
    print('first_name')
    return redirect('/')
  return render_template('show.html')

@app.route('/logout')
def logout():
  session.clear()
  return redirect('/')