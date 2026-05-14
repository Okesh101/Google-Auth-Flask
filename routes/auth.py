from flask import Blueprint, redirect, request, jsonify, session, url_for
from services.googleService import google_setup
from database.functions.onboarding import get_user_by_email, sign_up_user
from database.functions.profile import get_me
from datetime import datetime, timedelta, UTC
import jwt, os


auth_bp = Blueprint('auth_bp', __name__, url_prefix='/api/v1/auth')
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
            payload = { # Generating the payload to be sent alongside the JWT token
                "user_id": exists['id'],
                "email": exists['email'],
                "exp": datetime.now(UTC) + timedelta(hours=1)
            }
            token = jwt.encode( # Generating JWT token for the user
                payload,
                JWT_SECRET,
                algorithm="HS256"
            )

            return redirect(f"{FRONTEND_URL}?token={token}")
        
        # Signing up new user
        else: 
            created_user = sign_up_user( # Saving user in my database
                user_info.get("name"), 
                user_info.get("email"), 
                user_info.get("picture")
            )
            if created_user['code'] == 201: # Successfully created user in database
                user_data = created_user['data']
                payload = { # Generating the payload to be sent alongside the JWT token
                    "user_id": user_data['id'],
                    "email": user_data['email'],
                    "exp": datetime.now(UTC) + timedelta(hours=1)
                }
                token = jwt.encode( # Generating JWT token for the user
                    payload,
                    JWT_SECRET,
                    algorithm="HS256"
                )

                return redirect(f"{FRONTEND_URL}?token={token}")

            else:
                return redirect(f"{FRONTEND_URL}")
    
    except Exception as e:
        return jsonify({"status": "ERROR", 
                        "message": str(e), 
                        "code": 500}), 500


@auth_bp.route('/me', methods=['GET'])
def me_endpoint():
    try:
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"status": "ERROR", 
                            "message": "No token provided", 
                            "code": 401}), 401
        
        token = auth_header.split(" ")[1]
        decoded = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=["HS256"]
        )
        
        user_id = decoded["user_id"]
        
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