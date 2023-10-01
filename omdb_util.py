import os

import requests
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import sessionmaker

from models import Movie, User
from config import DATABASE_URI, OMDB_API_URL, OMDB_API_KEY
from session_manager import session, engine

# Check if the movies table exists, if not, create it
if not inspect(engine).has_table(Movie.__tablename__):
    Movie.metadata.create_all(engine)
# Check if the movies table exists, if not, create it
if not inspect(engine).has_table(User.__tablename__):
    User.metadata.create_all(engine)

# Fetch movies from OMDB API and save them to the database
def fetch_and_save_movies():
    if session.query(Movie).count() == 0:
        # Fetch 100 movies from OMDB API (you can customize the query)
        print('fetching movies from ommdb')
        api_url = OMDB_API_URL
        params = {
            "apikey": OMDB_API_KEY,
            "s": "movie",
            "type": "movie",
            "page": 1,
            "r": "json"
        }

        for _ in range(10):
            response = requests.get(api_url, params=params)
            data = response.json()

            if "Search" in data:
                for movie_data in data["Search"]:
                    title = movie_data["Title"]
                    # Save the movie to the database
                    movie = Movie(title=title)
                    session.add(movie)

            params["page"] += 1

        session.commit()


def fetch_movie_data_from_omdb(title):
    try:
        # Prepare the OMDB API request URL
        api_url = OMDB_API_URL
        params = {
            "apikey": OMDB_API_KEY,
            "t": title
        }

        # Send a GET request to OMDB API
        response = requests.get(api_url, params=params)
        response.raise_for_status()

        # Parse the JSON response
        movie_data = response.json()

        return movie_data

    except requests.exceptions.RequestException as e:
        return None
