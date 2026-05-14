from database.db import get_db_connection

def get_me(user_id):
    db = get_db_connection()
    try:
        cursor = db.cursor()
        cursor.execute("SELECT id, email, name, profile_pic FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        if user:
            return {
                "status": "SUCCESS", 
                "data": {
                    "id": user[0],
                    "email": user[1],
                    "name": user[2],
                    "picture": user[3]
                }, 
                "code": 200, 
                "message": "User details fetched successfully"
            }
        else:
            return {
                "status": "ERROR", 
                "message": "User not found", 
                "code": 404
            }
    except Exception as e:
        return {
            "status": "ERROR", 
            "message": str(e), 
            "code": 500
        }
    finally:
        if db:
            db.close()