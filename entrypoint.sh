#!/bin/bash

# Initialize the database
flask --app api.py initdb

# Run the Flask app
flask run --host=0.0.0.0 --port=8090
