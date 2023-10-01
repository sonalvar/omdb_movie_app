from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)

class User(db.Model):
    __tablename__ = "users"
    username = db.Column(db.String(255), primary_key=True)
    password = db.Column(db.String(255), nullable=False)
