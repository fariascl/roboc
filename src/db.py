import os
from dotenv import load_dotenv
import sqlite3
load_dotenv()


def get_db():
    DB_PATH = os.getenv('DB_PATH', 'roboc.db')
    conn = sqlite3.connect(DB_PATH)
    return conn