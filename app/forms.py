from flask_wtf import FlaskForm
from sqlalchemy import text
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, InputRequired
from app import models, db


class RegistrationForm(FlaskForm):
    user_name = StringField('Name', validators=[DataRequired('Please enter your name!'), Length(max=25)])
    password=PasswordField('Password', validators=[DataRequired('Please enter your password!'),Length(max=25)])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    user_name = StringField('Name', validators=[DataRequired('Please enter your name!'), Length(max=25)])
    password = PasswordField('Password', validators=[DataRequired('Please enter your password!'), Length(max=25)])
    submit = SubmitField('Register')

class RestockForm(FlaskForm):

    def __init__(self, *args, **kwargs):
        super(RestockForm, self).__init__(*args, **kwargs)
        self.set_book_and_bookstore()


    def set_book_and_bookstore(self):
        books=models.Book.query.all()
        bookstores= models.Bookstore.query.all()
        block_sets=db.session.execute(
            text("call get_block_with_bookstore_book(:Bookstore_name, :Book_name)"),
            {"Bookstore_name": bookstores[0].library_name, "Book_name": books[0].book_name}
        )
        block_sets=block_sets.fetchall()

        book_choices=[]
        bookstore_choices = []
        block_choices = []

        for i in range(len(books)):
            book_choices.append((books[i].book_name,books[i].book_name))
        for i in range(len(bookstores)):
            bookstore_choices.append((bookstores[i].library_name,bookstores[i].library_name))
        for i in range(len(block_sets)):
            block_choices.append((block_sets[i].available_capacity,block_sets[i].block_number))
        self.available_capacity.data = block_sets[0].available_capacity
        self.book.choices = book_choices
        self.bookstore.choices= bookstore_choices
        self.block_number.choices=block_choices

    bookstore = SelectField('Bookstore', validators=[DataRequired()])
    book = SelectField('Book', validators=[DataRequired()])
    block_number = SelectField('Block Number', validators=[DataRequired()])
    available_capacity = IntegerField('Available Capacity', render_kw={'readonly': True})
    quantity = StringField('Quantity', validators=[InputRequired()])
    submit_restock = SubmitField('Restock')

class CreateBookForm(FlaskForm):
    author = StringField('Author', validators=[InputRequired()])
    book_name = StringField('Book Name', validators=[InputRequired()])
    edition = StringField('Edition', validators=[InputRequired()])
    genre = StringField('Genre', validators=[InputRequired()])
    publisher = StringField('Publisher', validators=[InputRequired()])
    submit_create_book = SubmitField('Create New Book')