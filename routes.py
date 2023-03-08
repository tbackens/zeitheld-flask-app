from app import app, db, login_manager
from flask import render_template, request, flash, redirect, url_for
from forms import RegisterForm, LoginForm
from models import User
from flask_login import current_user, login_user, logout_user, login_required


"""
- Index Route -
"""
@app.route('/')
def index():
    return redirect(url_for('login'))


"""
- Dashboard Route -
User is getting redirected to the dashboard after logged in.
User can use logout button ad is then redirected to the logout route.
"""
@app.route('/dashboard/<user>', methods=['GET', 'POST'])
@login_required
def dashboard(user):
    if request.method == 'POST':
        if request.form.get('Logout') == 'logout':
            return redirect(url_for('logout'))
    return render_template('dashboard.html')


"""
- Signup Route -
User has to fill in data. After submitting, password hash will be created and user
is stored in database. Then, user is redirected to the login route.
"""
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        flash('You are already LoggedIn')
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.create_pw_hash(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Successfully registered')
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)


"""
- Login Route -
User has to fill in data. After submitting, data ist validated by quering the database. 
If data is valid, login_user() is called. Then, user is redirected to the dashboard route.
"""
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already LoggedIn')
        return redirect(url_for('dashboard', user=current_user.username))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_pw_hash(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('dashboard', user=current_user.username))

    return render_template('login.html', form=form)


"""
- Logout Route -
Redirection to login route after logout_user() was called.
"""
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

        

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()