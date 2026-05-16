# routes/google.py

from flask import Blueprint, redirect, jsonify, url_for
from services.googleService import google_setup
from database.functions.onboarding import get_user_by_email, sign_up_user
from database.functions.jwt_auth import save_refresh_token
from urllib.parse import quote
from datetime import datetime, timedelta, UTC
import os
import jwt

google_bp = Blueprint("google_bp", __name__, url_prefix="/api/v1/auth")

is_production = os.getenv("FLASK_ENV") == "production"
FRONTEND_URL = os.getenv("FRONTEND_URL")
JWT_SECRET = os.getenv("JWT_SECRET_KEY")
google = google_setup()


@google_bp.route('/google', methods=['GET'])
def google_login_endpoint():
    redirect_uri = url_for(
        'google_bp.auth_callback',
        _external=True
    )
    return google.authorize_redirect(redirect_uri)


@google_bp.route('/callback', methods=['GET'])
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
                "role": exists['role'],
                "exp": datetime.now(UTC) + timedelta(minutes=15),
                "type": "access"
            }

            refresh_payload = {  # Generating the payload to be sent alongside the JWT token (refresh_token)
                "user_id": exists["id"],
                "email": exists['email'],
                "role": exists['role'],
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

            refresh_token_result = save_refresh_token(
                exists["id"], refresh_token, datetime.now(UTC) + timedelta(days=30))
            
            if refresh_token_result['code'] != 200:
                return jsonify(refresh_token_result), refresh_token_result['code']

            encoded_access_token = quote(access_token)
            response = redirect(
                f"{FRONTEND_URL}/auth/callback?access_token={encoded_access_token}"
            )

            response.set_cookie(
                'refresh_token',
                refresh_token,
                httponly=True,
                secure=True if is_production else False,
                samesite="None" if is_production else "Lax",
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
                    "role": user_data['role'],
                    "exp": datetime.now(UTC) + timedelta(minutes=15),
                    "type": "access"
                }

                refresh_payload = {  # Generating the payload to be sent alongside the JWT token (refresh_token)
                    "user_id": user_data["id"],
                    "email": user_data['email'],
                    "role": user_data['role'],
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

                refresh_token_result = save_refresh_token(
                    user_data["id"], refresh_token, datetime.now(UTC) + timedelta(days=30))

                if refresh_token_result['code'] != 200:
                    return jsonify(refresh_token_result), refresh_token_result['code']

                encoded_access_token = quote(access_token)
                response = redirect(
                    f"{FRONTEND_URL}/auth/callback?access_token={encoded_access_token}"
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
