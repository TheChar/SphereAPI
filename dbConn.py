import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def getConn(dbname:str):
    conn = psycopg2.connect(
        host=os.getenv('DB_HOSTNAME'),
        dbname=dbname,
        user=os.getenv('DB_USERNAME'),
        password=os.getenv('DB_PASSWORD'),
        port=os.getenv('DB_PORT')
    )

    return conn