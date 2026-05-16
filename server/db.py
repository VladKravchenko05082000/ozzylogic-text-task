import sqlite3
import os
from contextlib import contextmanager

from lib.helpers import get_file_logger

from configs.db_config import (SCHEMA, DB_PATH)
from configs.error_logs_files_name import DB_ERROR_FILE_NAME

logger = get_file_logger(DB_ERROR_FILE_NAME)

@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        logger.exception("Database error")
        raise
    finally:
        conn.close()     


def init_db():
    db_dir = os.path.dirname(DB_PATH)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
        
    with get_conn() as conn:
        conn.executescript(SCHEMA)
        