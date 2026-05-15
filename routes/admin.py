from flask import Blueprint, request, jsonify
from middlewares.role_middleware import require_role
from middlewares.auth_middleware import require_auth

admin_bp = Blueprint("admin_bp", __name__, url_prefix="/api/v1/admin")

@admin_bp.route("/users", methods=['GET'])
@require_auth
@require_role("admin")
def get_users_endpoint():
    return  jsonify({
        "status": "SUCCESS",
        "code": 200,
        "message": "All users retrieved successfully by admin."
    }), 200
