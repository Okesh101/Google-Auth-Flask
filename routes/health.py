from flask import Blueprint, jsonify
from datetime import datetime

health_bp = Blueprint("health_bp", __name__, url_prefix="/api/v1")


@health_bp.route('/health', methods=['GET'])
def health_endpoint():
    return jsonify({
        "status": "SUCCESS",
        "code": 200,
        "message": f"Service is up and running at {datetime.now().isoformat().split("T")[1].split(".")[0]}"
    })
