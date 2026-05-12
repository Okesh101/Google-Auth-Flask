import os, sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "GoogleAuth.db")

def get_db_connection():
    conn = sqlite3.connect(DB_DIR)
    # This line lets you access columns by name: row['username']
    conn.row_factory = sqlite3.Row
    return conn


# Database Initialization & Table Creation
def init_db():
    conn = get_db_connection()
    try:
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        with open(schema_path, "r") as f:
            sql = f.read()

        conn.executescript(sql)
        conn.commit()
        print("✅ Database initialized successfully!") # Add this
    except Exception as e:
        print(f"❌ DATABASE INIT ERROR: {e}")  # Add this
        return {"status": "ERROR",
                "message": f"Error occurred while initializing database: {e}",
                "code": 500}
    finally:
        conn.close()
