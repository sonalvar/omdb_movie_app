# Flask Movie API

This is a simple Flask-based movie API that allows you to manage a list of movies. It provides endpoints for adding, removing, and retrieving movies.

## Getting Started

These instructions will help you set up and run the Flask application using Docker.

### Prerequisites

- [Docker](https://www.docker.com/get-started) installed on your machine.

### Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/sonalvar/omdb_movie_app.git
   ```

## Running the App
#### Using Python
To run the app using Python, execute the following command:

```
python api.py
```
The Flask app will be accessible at http://127.0.0.1:8090.

#### Using Docker Compose
If you prefer running the app using Docker Compose, make sure you have Docker installed and running on your machine. Then, execute the following command:

```
docker-compose up
```
The Flask app will be accessible at http://127.0.0.1:8090.

# API Endpoints
**/movies (GET)**: Retrieve a list of movies.\
**/movies/<int:id> (GET)**: Retrieve a movie by ID.\
**/movies/title/<string:title> (GET)**: Retrieve a movie by title.\
**/movies (POST)**: Add a new movie (requires authorization).\
**/movies/<int:id> (DELETE)**: Remove a movie by ID (requires authorization).\

# Authentication
To use the /movies (POST) and /movies/<int:id> (DELETE) endpoints, you need to include basic authentication headers:

**Username**: Your username\
**Password**: Your password

# Running Tests
To run the unit tests for the app, use the following command:
```
python -m unittest tests.test_api
```
The test cases should be detected and executed successfully.
