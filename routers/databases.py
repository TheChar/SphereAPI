from fastapi import APIRouter
from psycopg2 import sql
import psycopg2
import os
from ..dbConn import conn as ogConn

router = APIRouter(
    prefix='/databases'
)

"""Creates a database with given name

Returns:
    json: Complete message
"""
@router.put('/create')
async def createDatabase(name:str):
    conn = psycopg2.connect(
        host=os.getenv('DB_HOSTNAME'),
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USERNAME'),
        password=os.getenv('DB_PASSWORD'),
        port=os.getenv('DB_PORT')
    )

    conn.autocommit = True

    with open('scripts/createDatabase.sql') as f:
        query = f.read()

    query = sql.SQL(query).format(dbname=sql.Identifier(name))

    with conn.cursor() as cur:
        cur.execute(query)
    conn.autocommit = False

    conn.close()

    return {"message": "Operation Complete"}


"""Deletes a database

Returns:
    json: Complete message
"""
@router.delete('/delete')
async def deleteDatabase(name:str):
    conn = psycopg2.connect(
        host=os.getenv('DB_HOSTNAME'),
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USERNAME'),
        password=os.getenv('DB_PASSWORD'),
        port=os.getenv('DB_PORT')
    )

    conn.autocommit = True

    with open('scripts/dropDatabase.sql') as f:
        query = f.read()
        f.close()

    query = sql.SQL(query).format(dbname=sql.Identifier(name))

    with conn.cursor() as cur:
        cur.execute(query)
    conn.autocommit = False

    conn.close()

    return {"message": "Operation Complete"}


"""Lists databases on server

Returns:
    json: List of databases
"""
@router.get('/list')
async def listDatabases():
    with open('scripts/listDatabases.sql') as f:
        query = f.read()
    
    with ogConn.cursor() as cur:
        cur.execute(query)
        res = cur.fetchall()
    
    return res