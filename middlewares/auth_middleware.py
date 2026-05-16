# middlewares/auth_middleware.py

from functools import wraps
from flask import request, jsonify, g
import jwt
import os

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

def require_auth(func):
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Validate token
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"status": "ERROR",
                            "code": 400,
                            "message": "Authorization header missing"
                            }), 400
        
        if not auth_header.startswith("Bearer "):
            return jsonify({"status": "ERROR",
                            "code": 400,
                            "message": "Invalid token format"
                            }), 400
        
        # Decode Token
        token = auth_header.split(" ")[1]

        try:
            decoded = jwt.decode(
                token,
                JWT_SECRET_KEY,
                algorithms=["HS256"]
            )

            # Attach user
            g.user = decoded
        except jwt.ExpiredSignatureError:
            return jsonify({
                "status": "ERROR",
                "message": "Token expired",
                "code": 401
            }), 401

        except jwt.InvalidTokenError:
            return jsonify({
                "status": "ERROR",
                "message": "Invalid token",
                "code": 401
            }), 401
        
        return func(*args, **kwargs)
    return wrapper
