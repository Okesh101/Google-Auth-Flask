# routes/auth.py

from flask import Blueprint, request, jsonify, g
from middlewares.auth_middleware import require_auth
from database.functions.jwt_auth import verify_refresh_token, revoke_refresh_token
from database.functions.profile import get_me
from datetime import datetime, timedelta, UTC
import jwt
import os


auth_bp = Blueprint('auth_bp', __name__, url_prefix='/api/v1/auth')


JWT_SECRET = os.getenv("JWT_SECRET_KEY")


@auth_bp.route('/refresh', methods=['POST'])
def refresh_token_endpoint():
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        return jsonify({
            "status": "ERROR",
            "code": 401,
            "message": "Refresh token missing"
        }), 401

    try:
        decoded = jwt.decode(
            refresh_token,
            JWT_SECRET,
            algorithms=['HS256']
        )

        if decoded["type"] != "refresh":
            return jsonify({
                "status": "ERROR",
                "code": 401,
                "message": "Invalid token type"
            }), 401
        
        db_token = verify_refresh_token(refresh_token)
        if db_token['code'] != 200:
            return jsonify(db_token), db_token['code']
        
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

    
    new_access_payload = {
        "user_id": decoded["user_id"],
        "email": decoded["email"],
        "role": decoded["role"],
        "exp": datetime.now(UTC) + timedelta(minutes=15),
        "type": "access"
    }

    new_access_token = jwt.encode(
        new_access_payload,
        JWT_SECRET,
        algorithm="HS256"
    )

    return jsonify({
        "status": "SUCCESS",
        "code": 200,
        "message": "New access token generated successfully.",
        "access_token": new_access_token
    })


@auth_bp.route('/me', methods=['GET'])
@require_auth
def me_endpoint():
    try:
        user_id = g.user["user_id"]

        user_data = get_me(user_id)

        return jsonify(user_data), user_data['code']

    except Exception as e:
        return jsonify({"status": "ERROR",
                        "message": str(e),
                        "code": 500}), 500


@auth_bp.route('/logout', methods=['POST'])
@require_auth
def logout_endpoint():
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        return jsonify({
            "status": "ERROR",
            "code": 401,
            "message": "Refresh token missing"
        }), 401
    
    revoke_token_result = revoke_refresh_token(refresh_token)
    if revoke_token_result['code'] != 200:
        return jsonify(revoke_token_result), revoke_token_result['code']

    response = jsonify({
        "status": "SUCCESS",
        "code": 200,
        "message": "Loged out successfully."
    })

    response.delete_cookie("refresh_token")
    return response, 200