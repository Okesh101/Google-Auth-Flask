from flask import Blueprint, redirect, request, jsonify, session, url_for, g
from services.googleService import google_setup
from middlewares.auth_middleware import require_auth
from database.functions.onboarding import get_user_by_email, sign_up_user
from database.functions.profile import get_me
from datetime import datetime, timedelta, UTC
import jwt
import os


auth_bp = Blueprint('auth_bp', __name__, url_prefix='/api/v1/auth')


is_production = os.getenv("FLASK_ENV") == "production"
FRONTEND_URL = os.getenv("FRONTEND_URL")
JWT_SECRET = os.getenv("JWT_SECRET_KEY")
google = google_setup()


@auth_bp.route('/google', methods=['GET'])
def google_login_endpoint():
    redirect_uri = url_for(
        'auth_bp.auth_callback',
        _external=True
    )
    return google.authorize_redirect(redirect_uri)


@auth_bp.route('/callback', methods=['GET'])
def auth_callback():
    try:
        token = google.authorize_access_token()
        user_info = token.get("userinfo")

        exists = get_user_by_email(user_info.get("email"))

        # Signing in existing user
        if exists:

            access_payload = {  # Generating the payload to be sent alongside the JWT token (access_token)
                "user_id": exists['id'],
                "email": exists['email'],
                "exp": datetime.now(UTC) + timedelta(minutes=15),
                "type": "access"
            }

            refresh_payload = {  # Generating the payload to be sent alongside the JWT token (refresh_token)
                "user_id": exists["id"],
                "email": exists['email'],
                "exp": datetime.now(UTC) + timedelta(days=30),
                "type": "refresh"
            }

            access_token = jwt.encode(  # Generating JWT access token for the user
                access_payload,
                JWT_SECRET,
                algorithm="HS256"
            )

            refresh_token = jwt.encode(  # Generating JWT refresh token for the user
                refresh_payload,
                JWT_SECRET,
                algorithm="HS256"
            )

            response = redirect(
                f"{FRONTEND_URL}/auth/callback?access_token={access_token}"
            )

            response.set_cookie(
                'refresh_token',
                refresh_token,
                httponly=True,
                secure=True if is_production else False,
                samesite="Lax",
                max_age=60 * 60 * 24 * 30
            )

            return response

        # Signing up new user
        else:
            created_user = sign_up_user(  # Saving user in my database
                user_info.get("name"),
                user_info.get("email"),
                user_info.get("picture")
            )
            if created_user['code'] == 201:  # Successfully created user in database
                user_data = created_user['data']

                access_payload = {  # Generating the payload to be sent alongside the JWT token (access_token)
                    "user_id": user_data['id'],
                    "email": user_data['email'],
                    "exp": datetime.now(UTC) + timedelta(minutes=15),
                    "type": "access"
                }

                refresh_payload = {  # Generating the payload to be sent alongside the JWT token (refresh_token)
                    "user_id": user_data["id"],
                    "email": user_data['email'],
                    "exp": datetime.now(UTC) + timedelta(days=30),
                    "type": "refresh"
                }

                access_token = jwt.encode(  # Generating JWT access token for the user
                    access_payload,
                    JWT_SECRET,
                    algorithm="HS256"
                )

                refresh_token = jwt.encode(  # Generating JWT refresh token for the user
                    refresh_payload,
                    JWT_SECRET,
                    algorithm="HS256"
                )

                response = redirect(
                    f"{FRONTEND_URL}/auth/callback?access_token={access_token}"
                )

                response.set_cookie(
                    'refresh_token',
                    refresh_token,
                    httponly=True,
                    secure=True if is_production else False,
                    samesite="Lax",
                    max_age=60 * 60 * 24 * 30
                )

                return response

            else:
                return redirect(f"{FRONTEND_URL}/auth/callback")

    except Exception as e:
        return jsonify({"status": "ERROR",
                        "message": str(e),
                        "code": 500}), 500


@auth_bp.route('/refresh', methods=['POST'])
def refresh_token_endpoint():
    refresh_token = request.cookie.get("refresh_token")

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
    
    new_access_payload = {
        "user_id": decoded["user_id"],
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


@auth_bp.route('/logout', methods=['GET'])
def logout_endpoint():
    try:
        session.clear()
        return jsonify({"status": "SUCCESS",
                        "code": 200,
                        "message": "Logged out"}), 200
    except Exception as e:
        return jsonify({"status": "ERROR",
                        "message": str(e),
                        "code": 500}), 500


@auth_bp.route('/debug', methods=['GET'])
def debug_endpoint():
    try:
        return jsonify(dict(session)), 200
    except Exception as e:
        return jsonify({"status": "ERROR",
                        "message": str(e),
                        "code": 500}), 500
