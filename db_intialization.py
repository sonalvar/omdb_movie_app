# db_initialization.py
from flask import current_app

from models import Movie, User
from omdb_util import fetch_and_save_movies
from session_manager import session


def initdb_command():
    with current_app.app_context():
        # Your database initialization logic here
        db.create_all()
        print("Database initialization block executed.")
        if session.query(User).count() == 0:
            # If no users exist, create a test user
            test_user = User(username='test_user', password='password123')
            session.add(test_user)
            try:
                session.commit()
            except Exception as e:
                print(f"Error committing data to the database: {str(e)}")
        if session.query(Movie).count() == 0:
            fetch_and_save_movies()
