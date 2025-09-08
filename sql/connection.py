import mysql.connector
from mysql.connector import errorcode
from typing import Optional, Dict, Any
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api.MyInfo import MySQL_Password

# You can load these from env vars or a config file
DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root", 
    "password": MySQL_Password,
    "database": "lolstats", 
    "autocommit": True,
}

def get_conn(**overrides) -> mysql.connector.MySQLConnection:
    """Create a new DB connection. Use overrides to tweak per-call (e.g., database="other")."""
    cfg = {**DB_CONFIG, **overrides}
    try:
        return mysql.connector.connect(**cfg)
    except mysql.connector.Error as e:
        if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            raise RuntimeError("DB auth failed. Check user/password.") from e
        if e.errno == errorcode.ER_BAD_DB_ERROR:
            raise RuntimeError(f"Database {cfg.get('database')} does not exist.") from e
        raise
