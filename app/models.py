from datetime import datetime

from app import db

class Bookstore(db.Model):
    __tablename__ = 'bookstore'
    bookstore_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    street_number = db.Column(db.String(10))
    street_address = db.Column(db.String(30))
    town = db.Column(db.String(20))
    state = db.Column(db.String(20))
    zip_code = db.Column(db.String(20))
    library_name = db.Column(db.String(30), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)

class StoreBlock(db.Model):
    __tablename__ = 'store_block'
    block_number = db.Column(db.Integer, primary_key=True)

class Genre(db.Model):
    __tablename__ = 'genre'
    genre_name = db.Column(db.String(20), primary_key=True)

class StoreBlockGenre(db.Model):
    __tablename__ = 'store_block_genre'
    block_number = db.Column(db.Integer, db.ForeignKey('store_block.block_number'), primary_key=True)
    bookstore_id = db.Column(db.Integer, db.ForeignKey('bookstore.bookstore_id'), primary_key=True)
    genre_name = db.Column(db.String(20), db.ForeignKey('genre.genre_name'), primary_key=True)
    capacity = db.Column(db.Integer, nullable=False, default=0)
    available_capacity = db.Column(db.Integer, nullable=False, default=0)

class StoreBlockBook(db.Model):
    __tablename__ = 'store_block_book'
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'), primary_key=True)
    block_number = db.Column(db.Integer, db.ForeignKey('store_block.block_number'), primary_key=True)
    bookstore_id = db.Column(db.Integer, db.ForeignKey('bookstore.bookstore_id'), primary_key=True)
    stock = db.Column(db.Integer, nullable=False, default=0)

class Publisher(db.Model):
    __tablename__ = 'publisher'
    publisher_name = db.Column(db.String(50), primary_key=True)
    street_number = db.Column(db.String(10))
    street_address = db.Column(db.String(30))
    town = db.Column(db.String(10))
    state = db.Column(db.String(10))
    zip_code = db.Column(db.String(10))

class Book(db.Model):
    __tablename__ = 'book'
    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_name = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    edition = db.Column(db.Integer, nullable=False, default=1)
    descriptions = db.Column(db.Text)
    img_link = db.Column(db.String(50))
    publisher_name = db.Column(db.String(50), db.ForeignKey('publisher.publisher_name'))
    total_in_stock = db.Column(db.Integer, nullable=False, default=0)

class BookGenre(db.Model):
    __tablename__ = 'book_genre'
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'), primary_key=True)
    genre_name = db.Column(db.String(20), db.ForeignKey('genre.genre_name'), primary_key=True)



class BookPublisherStore(db.Model):
    __tablename__ = 'book_publisher_store'
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'), primary_key=True)
    publisher_name = db.Column(db.String(50), db.ForeignKey('publisher.publisher_name'), primary_key=True)
    bookstore_id = db.Column(db.Integer, db.ForeignKey('bookstore.bookstore_id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default=0)

class Orders(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_date = db.Column(db.Date, nullable=False)

class Customer(db.Model):
    __tablename__ = 'customer'
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_name = db.Column(db.String(50))
    pass_word = db.Column(db.String(50))
    is_admin = db.Column(db.Boolean, default=False)
    street_number = db.Column(db.String(10))
    street_address = db.Column(db.String(30))
    town = db.Column(db.String(10))
    state = db.Column(db.String(10))
    zip_code = db.Column(db.String(10))

class CustomerOrderBook(db.Model):
    __tablename__ = 'customer_order_book'
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default=0)



class OrderDetails(db.Model):
    __tablename__ = 'bookstore_book_orders'
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'), primary_key=True)
    bookstore_id = db.Column(db.Integer, db.ForeignKey('bookstore.bookstore_id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default=0)