from flask import render_template, url_for, flash, redirect, request
from flask_app.forms import RegisterForm, LoginForm
from flask_app import app, db, bcrypt
from flask_app.models import User, Book
from flask_login import login_user, logout_user, current_user, login_required

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash("You are already registered!", "info")
        return redirect(url_for('login'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data)
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        flash('User has been successfully created', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Register')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in!", "info")
        return redirect(url_for('books'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessfull. Please check email or password.', 'danger')
    return render_template('login.html', form=form, title='Login')

@app.route("/books", methods=['GET','POST'])
@login_required
def books():
    if not current_user.is_authenticated:
        flash("Please log in before accessing this page", "danger")
        return redirect(url_for('login'))
    books = Book.list_books()
    return render_template('books.html', title='Book Service', books=books)

@app.route("/borrow_book/<int:book_id>", methods=['GET','POST'])
@login_required
def borrow_book(book_id):
    if current_user.is_authenticated:
        book = Book.query.get(book_id)
        current_user.borrow_book(book)
        flash("Book has been borrowed!", 'success')
    else:
        flash("Please log in before accessing this page", "danger")
    return redirect(url_for('books'))

@app.route("/return_book/<int:book_id>", methods=['GET','POST'])
@login_required
def return_book(book_id):
    if current_user.is_authenticated:
        book = Book.query.get(book_id)
        current_user.return_book(book)
        flash("Book has been returned!", 'success')
    else:
        flash("Please log in before accessing this page", "danger")
    return redirect(url_for('profile'))

@app.route("/profile", methods=['GET','POST'])
@login_required
def profile():
    if not current_user.is_authenticated:
        flash("Please log in before accessing this page", "danger")
        return redirect(url_for('login'))
    borrowed_books = current_user.borrowed_books
    return render_template('profile.html', title='Borrowed Books', borrowed_books=borrowed_books)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You were logged out!", "info")
    return redirect(url_for('home'))