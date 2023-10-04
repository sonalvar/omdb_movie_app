# auth.py
from functools import wraps
from flask import request, g, jsonify
from models import User
from session_manager import session

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
