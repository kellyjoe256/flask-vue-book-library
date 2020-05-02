from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import (
    gen_salt, generate_password_hash, check_password_hash)
from app.helpers import abort_with_json

db = SQLAlchemy()


class TimestampMixin(object):
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, onupdate=datetime.now, default=datetime.now)


class CRUDMixin(object):

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find(cls, id, load_options=None):
        entity = None

        if not load_options:
            entity = cls.query.get(id)
        else:
            entity = cls.query.options(load_options).get(id)

        return entity

    @classmethod
    def find_or_fail(cls, id, load_options=None):
        entity = cls.find(id, load_options)

        if not entity:
            data = dict(
                message='{} not found'.format(cls.__name__)
            )
            abort_with_json(404, data)

        return entity


class User(db.Model, TimestampMixin, CRUDMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    salt = db.Column(db.String(32))
    hashed_password = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User {!r}>'.format(self.username)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        salt = gen_salt(32)
        self.salt = salt
        self.hashed_password = generate_password_hash(password + salt)

    def verify_password(self, password):
        return check_password_hash(self.hashed_password, password + self.salt)

    def json(self):
        return dict(
            id=self.id,
            username=self.username,
            created_at=str(self.created_at),
            is_admin=self.is_admin,
        )


books_authors = db.Table('books_authors',
                         db.Column('book_id', db.Integer,
                                   db.ForeignKey('books.id',
                                                 ondelete='CASCADE'),
                                   primary_key=True),
                         db.Column('author_id', db.Integer,
                                   db.ForeignKey('authors.id',
                                                 ondelete='CASCADE'),
                                   primary_key=True))


books_categories = db.Table('books_categories',
                            db.Column('book_id', db.Integer,
                                      db.ForeignKey('books.id',
                                                    ondelete='CASCADE'),
                                      primary_key=True),
                            db.Column('category_id', db.Integer,
                                      db.ForeignKey('categories.id',
                                                    ondelete='CASCADE'),
                                      primary_key=True))


class Category(db.Model, CRUDMixin):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    # books = db.relationship('Book', secondary=books_categories,
    #                              backref=db.backref('books',
    #                                                 lazy=True))

    def __repr__(self):
        return '<Category {}>'.format(self.name)

    def json(self):
        return dict(id=self.id, name=self.name,)


class Author(db.Model, TimestampMixin, CRUDMixin):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.Enum("M", "F", name="author_gender"))
    about = db.Column(db.Text, nullable=False)

    books = db.relationship('Book', secondary=books_authors,
                            backref=db.backref('books', lazy=True))

    def __repr__(self):
        return '<Author {}>'.format(self.last_name + " " + self.first_name)

    def json(self):
        return dict(
            id=self.id,
            last_name=self.last_name,
            first_name=self.first_name,
            gender=self.gender,
            about=self.about,
        )


class Book(db.Model, TimestampMixin, CRUDMixin):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    num_of_pages = db.Column(db.Integer, nullable=False)
    publisher = db.Column(db.String(100), nullable=False)
    publication_date = db.Column(db.Date, nullable=False)
    about = db.Column(db.Text, nullable=False)

    authors = db.relationship('Author', secondary=books_authors,
                              backref=db.backref('authors', lazy=True))
    categories = db.relationship('Category', secondary=books_categories,
                                 backref=db.backref('categories',
                                                    lazy=True))

    def __repr__(self):
        return '<Book {0}>'.format(self.title)

    def json(self):
        return dict(
            id=self.id,
            isbn=self.isbn,
            title=self.title,
            num_of_pages=self.num_of_pages,
            publisher=self.publisher,
            publication_date=str(self.publication_date),
            about=self.about,
        )
