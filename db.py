import os
from dotenv import load_dotenv
import pymysql
load_dotenv()


def get_db():
    conn = pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    conn.autocommit = True
    return conn

    