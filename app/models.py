from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import (
    gen_salt, generate_password_hash, check_password_hash)

db = SQLAlchemy()


class TimestampMixin(object):
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, onupdate=datetime.now, default=datetime.now)


class SaveDeleteMixin(object):

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class User(db.Model, TimestampMixin, SaveDeleteMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    salt = db.Column(db.String(32))
    hashed_password = db.Column(db.String(128))

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
        return {
            'id': self.id,
            'username': self.username,
            'created_at': str(self.created_at),
        }
