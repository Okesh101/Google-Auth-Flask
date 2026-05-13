from flask import Blueprint, redirect, request, jsonify, session, url_for
from services.googleService import google_setup
from database.functions.onboarding import get_user_by_email, sign_up_user


auth_bp = Blueprint('auth_bp', __name__, url_prefix='/api/v1/auth')
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

        if exists:
            session["user"] = {
                "id": exists['id'],
                "email": exists['email'],
                "name": exists['name'],
                "picture": exists['profile_pic']
            }
        else:
            result = sign_up_user(
                user_info.get("name"), 
                user_info.get("email"), 
                user_info.get("picture")
            )
            if result['code'] == 201:
                session["user"] = {
                    "email": user_info.get("email"),
                    "name": user_info.get("name"),
                    "picture": user_info.get("picture")
                }

        return redirect("http://127.0.0.1:5173/dashboard")
    
    except Exception as e:
        return jsonify({"status": "ERROR", 
                        "message": str(e), 
                        "code": 500}), 500


@auth_bp.route('/me', methods=['GET'])
def me_endpoint():
    try:
        user = session.get("user")
        if not user:
            return jsonify({"status": "ERROR", 
                            "message": "User not authorized", 
                            "code": 401}), 401

        return jsonify({"status": "SUCCESS", 
                        "data": user, 
                        "code": 200, 
                        "message": "User details fetched successfully"}), 200
    
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