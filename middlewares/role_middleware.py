from functools import wraps
from flask import jsonify, g

def require_role(role):
    def decorator(func):
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_role = g.user.get("role")

            if user_role != role:
                return jsonify({
                    "status": "ERROR",
                    "code": 403,
                    "message": "Resource forbidden"
                }), 403
            
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator
