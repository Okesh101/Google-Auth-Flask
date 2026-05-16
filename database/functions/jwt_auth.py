# database/functions/jwt_auth.py

from database.db import get_db_connection
from datetime import datetime, UTC
import uuid
import sqlite3


def save_refresh_token(user_id, refresh_token, expires_at):
    db = get_db_connection()
    try:
        id = str(uuid.uuid4())

        expires_at_str = expires_at.isoformat()

        cursor = db.cursor()
        cursor.execute("""INSERT INTO refresh_tokens (id, user_id, token, expires_at)
                          VALUES (?, ?, ?, ?)""", 
                          (id, user_id, refresh_token, expires_at_str,)
                        )

        db.commit()
        return {
            "status": "SUCCESS",
            "code": 200,
            "id": id,
            "token": refresh_token,
            "message": "Refresh token saved successfully."
        }
    except sqlite3.IntegrityError as e:
        if db:
            db.rollback()
        return {
            "status": "ERROR",
            "code": 500,
            "message": f"Refresh token already exists: {e}."
        }
    except sqlite3.Error as e:
        if db:
            db.rollback()
        return {
            "status": "ERROR",
            "code": 500,
            "message": f"Error saving refresh token: {e}."
        }
    finally:
        if db:
            db.close()
        
    
def verify_refresh_token(token):
    db = get_db_connection()
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM refresh_tokens WHERE token = ?", (token,))
        row = cursor.fetchone()

        if row is None:
            return {
                "status": "ERROR",
                "code": 404,
                "message": "Refresh token not found in database."
            }
        
        if row['revoked'] == 1:
            return {
                "status": "ERROR",
                "code": 401,
                "message": "Token has been revoked. You must log in again."
            }
        
        expires_at = datetime.fromisoformat(row['expires_at'])
        if expires_at < datetime.now(UTC):
            return {
                "status": "ERROR",
                "code": 401,
                "message": "Token has expired. You must log in again."
            }
        
        return {
            "status": "SUCCESS",
            "code": 200,
            "message": "Token validation successful.",
            "token": row['token']
        }
    except sqlite3.Error as e:
        return {
            "status": "ERROR",
            "code": 500,
            "message": f"Error verifying refresh token: {e}."
        }
    finally:
        if db:
            db.close()


def revoke_refresh_token(refresh_token):
    db = get_db_connection()
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM refresh_tokens WHERE token = ?", (refresh_token,))
        row = cursor.fetchone()

        if row is None:
            return {
                "status": "ERROR",
                "code": 404,
                "message": "Token not found in database."
            }
        
        cursor.execute("UPDATE refresh_tokens SET revoked = 1 WHERE token = ?", (refresh_token,))

        db.commit()
        return {
            "status": "SUCCESS",
            "code": 200,
            "message": "Refresh token successfully revoked."
        }
    except sqlite3.Error as e:
        if db:
            db.rollback()
        return {
            "status": "ERROR",
            "code": 500,
            "message": f"Error revoking refresh token."
        }
    finally:
        if db:
            db.close()

        

