from flask import render_template, flash, session, redirect, url_for, request
from os.path import join, dirname, realpath
import os
from app import app, db
from .forms import RegistrationForm, LoginForm, RestockForm, CreateBookForm
import datetime
from datetime import timedelta
import json
import random
from flask import make_response, jsonify, abort
from .models import Customer, Orders, StoreBlockBook, Book, Bookstore, Publisher, Genre, BookGenre
import socket
import uuid
from sqlalchemy import text
from functools import wraps


def require_user_name(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        if 'user_name' not in session.keys():
            # Redirect to a login page or perform any action you prefer
            return redirect(url_for('login'))

        return func(*args, **kwargs)

    return wrapper

def admin_redirect(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        if 'user_name' not in session.keys():
            # Redirect to a login page or perform any action you prefer
            return redirect(url_for('login'))
        elif 'admin' not in session.keys() or session['admin']== False:
            return redirect(url_for('home'))
        return func(*args, **kwargs)

    return wrapper

@app.route('/')
def home():
    show_icon = False

    user_name=None

    if 'user_name' in session.keys():
        show_icon = True;
        user_name=session['user_name']

    book_set = db.session.execute(text("CALL get_all_books()"))
    book_set1 = book_set.fetchall()

    books = [dict(zip(book_set.keys(), row)) for row in book_set1]
    for book in books:
        if book['genres']:
            book['genres'] = book['genres'].split(',')
    return render_template('home.html', books=books, show_icon=show_icon, user_name=user_name)


@app.route('/search/<type>/<keyword>')
def search_result(type, keyword):
    texts = None

    show_icon = False
    user_name = None
    if 'user_name' in session.keys():
        show_icon = True
        user_name=session['user_name']

    if type == 'default':
        texts = text("CALL get_book_with_keyword(:keyword)")
    elif type == 'author':
        texts = text("CALL get_book_with_author(:keyword)")
    else:
        texts = text("CALL get_book_with_genre(:keyword)")
    keyword = keyword.strip().lower()
    book_set = db.session.execute(
        texts,
        {"keyword": keyword}
    )
    book_set1 = book_set.fetchall()
    books = [dict(zip(book_set.keys(), row)) for row in book_set1]
    for book in books:
        if book['genres']:
            book['genres'] = book['genres'].split(',')
    return render_template('home.html', books=books, show_icon=show_icon, user_name=user_name)


@app.route('/api/search/<keyword>', methods=['GET'])
def search_items(keyword):
    keyword = keyword.strip().lower()

    result_set = db.session.execute(
        text("CALL get_book_with_keyword(:keyword)"),
        {"keyword": keyword}
    )
    results = result_set.fetchall()
    data = []
    for row in results:
        data.append(row.book_name)
    return jsonify(data)


@app.route('/login', methods=['GET', 'POST'])
@require_user_name
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user_name = form.user_name.data
        existing_user = Customer.query.filter_by(customer_name=user_name).first()
        if existing_user is None:
            message = 'Username not exists.'
            return render_template('log_in.html', form=form, message=message)
        elif existing_user.pass_word != form.password.data:
            # Add the code to save the user registration data to the database
            message = 'Wrong password.'
            return render_template('log_in.html', form=form, message=message)
        else:
            session['user_name'] = user_name
            if existing_user.is_admin is True:
                session['admin'] = True
                return redirect(url_for('admin'))
            return redirect(url_for('home'))

    return render_template('log_in.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
@require_user_name
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user_name = form.user_name.data
        existing_user = Customer.query.filter_by(customer_name=user_name).first()
        if existing_user:
            message = 'Username already exists. Please choose a different username.'
            return render_template('register.html', form=form, message=message)
        else:
            # Add the code to save the user registration data to the database
            new_user = Customer(customer_name=user_name, pass_word=form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful!', 'success')
            session['user_name'] = user_name
            return redirect(url_for('home'))

    return render_template('register.html', form=form)


@app.route('/user_profile', methods=['GET', 'POST'])
@require_user_name
def user_profile():

    user_name=session['user_name']

    result_set = db.session.execute(
        text("call get_order_with_user_name(:user_name)"),
        {"user_name": user_name}
    )
    result_set = result_set.fetchall()

    user = Customer.query.filter_by(customer_name=user_name).first()

    '''
    books = [dict(zip(book_set.keys(), row)) for row in book_set1]
    for book in books:
        if book['genres']:
            book['genres'] = book['genres'].split(',')
    '''
    return render_template('user_profile.html', user=user)

@app.route('/api/order/<book_name>/<purchase>', methods=['GET'])
@require_user_name
def order_item(book_name, purchase):
    if 'id' not in session.keys():
        new_order = Orders(order_date=datetime.now())
        db.session.add(new_order)
        db.session.commit()
        new_order_id = new_order.order_id
        session['id']=new_order_id

    order_id = session['id']
    user_name = session['user_name']
    db.session.execute(
        text("call get_books_from_book_stores(:user_name, :Book_name, :purchase, :Order_id)"),
        {"user_name": user_name, "Book_name": book_name, "purchase": purchase, "Order_id":order_id}
    )

@app.route('/admin', methods=['GET'])
@admin_redirect
def admin():
    restock_form = RestockForm()
    create_book_form = CreateBookForm()
    if restock_form.validate_on_submit():
        new_restock= StoreBlockBook(book_id=Book.query.filter_by(book_name=restock_form.book.data).first().book_id,
                                    bookstore_id=Bookstore.query.filter_by(library_name=restock_form.bookstore.data).first().bookstore_id,
                                    block_number=restock_form.block_number.data,
                                    quantity=restock_form.quantity.data)
        db.session.add(new_restock)
        db.session.commit()
    if create_book_form.validate_on_submit():
        new_publisher=Publisher(publisher_name=create_book_form.publisher.data)
        db.session.add(new_publisher)
        db.session.commit()
        new_book = Book(book_name=create_book_form.book_name.data,
                        author=create_book_form.author.data,
                        edition=create_book_form.edition.data,
                        description=None,
                        img_link='/img/images.jpg',
                        publisher_name=create_book_form.publisher.data,
                        total_in_stock=0)
        db.session.add(new_book)
        db.session.commit()
        genres=create_book_form.genre.data.split(',')
        for genre in genres:
            if len(Genre.query.filter_by(genre_name=genre).all())==0:
                new_genre=Genre(genre_name=genre)
                db.session.add(new_genre)
                db.session.commit()
            new_book_genre = BookGenre(book_id=new_book.book_id, genre_name=genre)
            db.session.add(new_book_genre)
            db.session.commit()
    return render_template('admin.html', restock_form=restock_form, create_book_form=create_book_form)

@app.route('/api/search_block/<book>/<book_store>', methods=['GET'])
def search_block(book, book_store):
    book=book.replace('_', ' ')
    book_store = book_store.replace('_', ' ')
    block_sets = db.session.execute(
        text("call get_block_with_bookstore_book(:Bookstore_name, :Book_name)"),
        {"Bookstore_name": book_store, "Book_name": book}
    )
    block_sets = block_sets.fetchall()
    data=[]

    for i in range(len(block_sets)):
        data.append((str(i), block_sets[i].block_number))
    return jsonify(data)