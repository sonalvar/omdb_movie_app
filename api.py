from functools import wraps

from flask import Flask, jsonify, request, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS

from omdb_util import fetch_and_save_movies, fetch_movie_data_from_omdb
from models import db, Movie, User
from config import DATABASE_URI, OMDB_API_URL, OMDB_API_KEY
from session_manager import session

app = Flask(__name__)
CORS(app)

# Configure the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['DEFAULT_ITEMS_PER_PAGE'] = 10
app.config['OMDB_API_URL'] = OMDB_API_URL
app.config['OMDB_API_KEY'] = OMDB_API_KEY

db.init_app(app)

# Create a decorator for authorization
def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.authorization

        if not auth or not auth.username or not auth.password:
            return jsonify({"message": "Authorization required"}), 401

        user = session.query(User).filter(User.username == auth.username).first()

        if user and user.password == auth.password:
            g.user = user
            return f(*args, **kwargs)
        else:
            return jsonify({"message": "Unauthorized"}), 401
    return decorated_function

# Endpoint to get all movies, paginated
@app.route('/movies', methods=['GET'])
def get_movies():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', app.config['DEFAULT_ITEMS_PER_PAGE'], type=int)

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

# Endpoint to get movie by id
@app.route('/movies/<int:id>', methods=['GET'])
def get_movie(id):
    movie = session.query(Movie).filter(Movie.id == id).first()
    if movie:
        return jsonify({"id": movie.id, "title": movie.title})
    else:
        return jsonify({"message": "Movie not found"}), 404

# Endpoint to get movie by title
@app.route('/movies/title/<string:title>', methods=['GET'])
def get_movie_by_title(title):
    movie = session.query(Movie).filter(Movie.title == title).first()
    if movie:
        return jsonify({"id": movie.id, "title": movie.title})
    else:
        return jsonify({"message": "Movie not found"}), 404


# Endpoint to add a new movie
@app.route('/movies', methods=['POST'])
@authorize
def add_movie():
    data = request.get_json()
    title = data.get("title")

    if not title:
        return jsonify({"message": "Title is required"}), 400

    omdb_movie_data = fetch_movie_data_from_omdb(title)

    if not omdb_movie_data:
        return jsonify({"message": "Movie does not exst in OMDB"}), 400

    # Save the movie to the database
    movie = Movie(title=omdb_movie_data['Title'])
    session.add(movie)
    try:
        session.commit()
        return jsonify({"message": "Movie added successfully", "id": movie.id}), 201
    except IntegrityError:
        session.rollback()
        return jsonify({"message": "Movie already exists"}), 400

# Endpoint to remove a movie by ID
@app.route('/movies/<int:id>', methods=['DELETE'])
@authorize
def remove_movie(id):
    movie = session.query(Movie).filter(Movie.id == id).first()
    if movie:
        session.delete(movie)
        session.commit()
        return jsonify({"message": "Movie deleted successfully"})
    else:
        return jsonify({"message": "Movie not found"}), 404


# Flask CLI command to initialize the database
@app.cli.command("initdb")
def initdb_command():
    with app.app_context():
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8090, debug=True)
