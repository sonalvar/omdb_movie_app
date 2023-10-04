from api import app
from models import Movie
from omdb_util import fetch_movie_data_from_omdb
from session_manager import session
from flask import jsonify
from sqlalchemy.exc import IntegrityError


def add_movie(data):
    title = data.get("title")
    if not title:
        return jsonify({"message": "Title is required"}), 400
    
    omdb_movie_data = fetch_movie_data_from_omdb(title)

    if not omdb_movie_data:
        return jsonify({"message": "Movie does not exst in OMDB"}), 400

    # Save the movie to the database
    return save_movie_to_db(omdb_movie_data['Title'])


def save_movie_to_db(title):
    movie = Movie(title=title)
    session.add(movie)
    try:
        session.commit()
        return jsonify({"message": "Movie added successfully", "id": movie.id}), 201
    except IntegrityError:
        session.rollback()
        return jsonify({"message": "Movie already exists"}), 400


def get_movies(page, per_page):
    movies_query = session.query(Movie).order_by(Movie.title)

    total_count = movies_query.count()

    offset = (page - 1) * per_page
    # Perform the query with limit and offset
    movies = movies_query.limit(per_page).offset(offset).all()

    movie_list = []
    for movie in movies:
        movie_list.append({"id": movie.id, "title": movie.title})
    
    return jsonify({
        "movies": movie_list,
        "page": page,
        "per_page": per_page,
        "total_items": total_count
    })


def get_movie_by_id(id):
    movie = session.query(Movie).filter(Movie.id == id).first()
    if movie:
        return jsonify({"id": movie.id, "title": movie.title})
    else:
        return jsonify({"message": "Movie not found"}), 404


def get_movie_by_title(title):
    movie = session.query(Movie).filter(Movie.title == title).first()
    if movie:
        return jsonify({"id": movie.id, "title": movie.title})
    else:
        return jsonify({"message": "Movie not found"}), 404


def remove_movie(id):
    movie = session.query(Movie).filter(Movie.id == id).first()
    if movie:
        session.delete(movie)
        session.commit()
        return jsonify({"message": "Movie deleted successfully"})
    else:
        return jsonify({"message": "Movie not found"}), 404
