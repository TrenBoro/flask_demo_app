from flask_app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

borrowed_books = db.Table(
    'borrowed_books',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True),
    db.Column('borrow_date', db.DateTime, default=datetime.utcnow)
)

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    borrowed_books = db.relationship('Book', secondary=borrowed_books, backref=db.backref('users', lazy=True))

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def __repr__(self):
        return f"({self.first_name} {self.last_name} {self.email})"
    
    def borrow_book(self, book):
        if book not in self.borrowed_books:
            if book.in_stock():
                self.borrowed_books.append(book)
                db.session.commit()
    
    def return_book(self, book):
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)
            db.session.commit()
        
    @staticmethod
    def get_users():
        print('Users')
        users = User.query.all()
        for user in users:
            print(user)

class Book(db.Model):
    __tablename__ = 'book'

    STOCK = 20

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(60), nullable=False)

    borrowers = db.relationship('User', secondary=borrowed_books, backref=db.backref('books', lazy='dynamic'), lazy='dynamic')

    def __init__(self, title, author):
        self.title = title
        self.author = author
    
    def __repr__(self):
        return f"{self.title} by {self.author}"
    
    def in_stock(self):
        return self.borrowers.count() < self.STOCK

    def books_left(self):
        return self.STOCK - self.borrowers.count()
    
    '''
    list_books is for listing all the books on the site
    '''
    @staticmethod
    def list_books():
        books = Book.query.all()
        return books
