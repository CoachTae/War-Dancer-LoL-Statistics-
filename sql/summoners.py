from typing import Optional, Dict, Any
import mysql.connector

def get_stale_summoner(conn: mysql.connector.MySQLConnection) -> Optional[Dict[str, Any]]:
    """
    Return the least-recently-updated summoner as a dict (or None if table empty).
    Assumes LastUpdated is TIMESTAMP or DATETIME.
    """
    q = """
        SELECT *
        FROM summoners
        ORDER BY COALESCE(LastUpdated, '1970-01-01 00:00:00') ASC
        LIMIT 1
    """
    with conn.cursor(dictionary=True) as cur:
        cur.execute(q)
        return cur.fetchone()

def stamp_last_updated(conn: mysql.connector.MySQLConnection, puuid: str) -> None:
    """Set LastUpdated = NOW() for the given PUUID."""
    with conn.cursor() as cur:
        cur.execute("UPDATE summoners SET LastUpdated = NOW() WHERE puuid = %s", (puuid,))

