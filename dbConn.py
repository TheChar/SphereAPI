import psycopg2
import os

conn = psycopg2.connect(
    host=os.getenv('DB_HOSTNAME'),
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USERNAME'),
    password=os.getenv('DB_PASSWORD'),
    port=os.getenv('DB_PORT')
)