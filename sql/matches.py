from typing import Tuple, Optional
import mysql.connector
from mysql.connector import errorcode

def split_match_id(raw: str) -> Tuple[str, int]:
    """Split 'NA1_5197758177' -> ('NA1', 5197758177)"""
    platform, num = raw.split("_", 1)  # split once at the first underscore
    return platform, int(num)

def match_exists(conn: mysql.connector.MySQLConnection, platform: str, matchid: int) -> bool:
    """Return True if a (platform, matchid) row exists in matches."""
    sql = """
        SELECT 1
        FROM matches
        WHERE platform = %s AND matchid = %s
        LIMIT 1
    """
    with conn.cursor() as cur:
        cur.execute(sql, (platform, matchid))
        return cur.fetchone() is not None

def insert_match(conn: mysql.connector.MySQLConnection, platform: str, matchid: int, patch: str) -> None:
    """
    Insert a match row if missing. Works best when you have either:
      - PRIMARY KEY(platform, matchid), or
      - UNIQUE(platform, matchid)
    """
    sql = "INSERT IGNORE INTO matches (platform, matchid) VALUES (%s, %s)"
    with conn.cursor() as cur:
        cur.execute(sql, (platform, matchid, patch))


def ensure_partition(conn, patch):
    part_name = "p"+str(patch)
    part_name = part_name.replace(".", "_")
    print(part_name)
    
    # See if partition exists
    q = """
        SELECT 1
        FROM INFORMATION_SCHEMA.PARTITIONS
        WHERE TABLE_SCHEMA = DATABASE()
            AND TABLE_NAME = 'matches'
            AND PARTITION_NAME = %s
        LIMIT 1
    """
    with conn.cursor() as cur:
        cur.execute(q, (part_name,))
        if cur.fetchone():
            return False # partition already exists

    # Try to add it. If another process just added it, swallow the duplicate error
    alter = f"ALTER TABLE matches ADD PARTITION (PARTITION {part_name} VALUES IN (%s))"
    try:
        with conn.cursor() as cur:
            cur.execute(alter, (patch,))
        return True # Added new partition
    except mysql.connector.Error as e:
        if e.errno == errorcode.ER_PARTITION_MGMT_ON_NONPARTITIONED:
            raise RuntimeError("'matches' is not partitioned yet. Run the ALTER ... PARTITION BY first.") from e
        if e.errno in (errorcode.ER_SAME_NAME_PARTITION,):
            return
        raise
