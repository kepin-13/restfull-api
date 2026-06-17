from flask import request, jsonify
from functools import wraps
import jwt
from db import JWT_SECRET

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"message": "Akses ditolak. Token tidak ditemukan."}), 401

        try:
            data = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            request.user_data = data
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token sudah kedaluwarsa."}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token tidak valid atau palsu."}), 401

        return f(*args, **kwargs)
    return decorated