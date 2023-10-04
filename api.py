from db_initialization import initdb_command
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

import movie_controller
from auth import authorize
from config import DATABASE_URI, OMDB_API_KEY, OMDB_API_URL
from models import Movie, User, db
from omdb_util import fetch_and_save_movies, fetch_movie_data_from_omdb
from session_manager import session

app = Flask(__name__)
CORS(app)

# Configure the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['DEFAULT_ITEMS_PER_PAGE'] = 10
app.config['OMDB_API_URL'] = OMDB_API_URL
app.config['OMDB_API_KEY'] = OMDB_API_KEY

db.init_app(app)


# Endpoint to get all movies, paginated
@app.route('/movies', methods=['GET'])
def get_movies():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', app.config['DEFAULT_ITEMS_PER_PAGE'], type=int)
    except ValueError:
        return jsonify({'error': 'Invalid page or per_page values'}), 400
    return movie_controller.get_movies(page, per_page)


# Endpoint to get movie by id
@app.route('/movies/<int:id>', methods=['GET'])
def get_movie(id):
    return movie_controller.get_movie_by_id(id)


# Endpoint to get movie by title
@app.route('/movies/title/<string:title>', methods=['GET'])
def get_movie_by_title(title):
    return movie_controller.get_movie_by_title(title)


# Endpoint to add a new movie
@app.route('/movies', methods=['POST'])
@authorize
def add_movie():
    data = request.get_json()
    return movie_controller.add_movie(data)


# Endpoint to remove a movie by ID
@app.route('/movies/<int:id>', methods=['DELETE'])
@authorize
def remove_movie(id):
    return movie_controller.remove_movie(id)


# Flask CLI command to initialize the database
@app.cli.command("initdb")
def initdb_command():
    initdb_command()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8090, debug=True)
