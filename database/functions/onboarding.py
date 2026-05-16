# database/functions/onboarding.py

from database.db import get_db_connection
import sqlite3
import uuid


def sign_up_user(name, email, profile_pic="", role="user"):
    db = get_db_connection()
    try:
        cursor = db.cursor()
        user_id = str(uuid.uuid4())
        cursor.execute(
            """INSERT INTO users (id, email, name, profile_pic, role)
            VALUES (?, ?, ?, ?, ?)
            """, (user_id, email, name, profile_pic, role)
        )

        db.commit()
        return {
            "status": "CREATED",
            "code": 201,
            "message": "User successfully signed up.",
            "data": {
                "id": user_id,
                "name": name,
                "email": email,
                "role": role,
                "picture": profile_pic
            }
        }
    except sqlite3.IntegrityError as e:
        if db:
            db.rollback()
        return {
            "status": "ERROR",
            "code": 500,
            "message": f"User email already exists: {e}."
        }
    except sqlite3.Error as e:
        if db:
            db.rollback()
        return {
            "status": "ERROR",
            "code": 500,
            "message": f"Error signing up user: {e}."
        }
    finally:
        if db:
            db.close()


def get_user_by_email(email):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    return cursor.fetchone()
