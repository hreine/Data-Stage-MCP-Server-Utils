import sqlite3
import time
import json
import hashlib

CACHE_DB = 'cache.db'
CACHE_DURATION = 300  # 5 minutes in seconds

def _get_db_connection():
    conn = sqlite3.connect(CACHE_DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_cache_db():
    conn = _get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_cache (
            key TEXT PRIMARY KEY,
            data TEXT,
            timestamp INTEGER
        )
    """)
    conn.commit()
    conn.close()

def get_from_cache(key):
    conn = _get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT data, timestamp FROM job_cache WHERE key = ?", (key,))
    row = cursor.fetchone()
    conn.close()

    if row:
        data, timestamp = row['data'], row['timestamp']
        if (time.time() - timestamp) < CACHE_DURATION:
            return json.loads(data)
    return None

def set_cache(key, data):
    conn = _get_db_connection()
    cursor = conn.cursor()
    timestamp = int(time.time())
    json_data = json.dumps(data)
    cursor.execute(
        "INSERT OR REPLACE INTO job_cache (key, data, timestamp) VALUES (?, ?, ?)",
        (key, json_data, timestamp)
    )
    conn.commit()
    conn.close()

def generate_cache_key(*args, **kwargs):
    """Generates a unique cache key based on function arguments."""
    # Convert args and kwargs to a consistent string representation
    # This might need refinement depending on the complexity of arguments
    # For simplicity, we'll just stringify them and hash
    arg_string = json.dumps(args, sort_keys=True) + json.dumps(kwargs, sort_keys=True)
    return hashlib.md5(arg_string.encode('utf-8')).hexdigest()

# Initialize the database when the module is imported
init_cache_db()

