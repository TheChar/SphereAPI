"""
Routes: /system/database/* => create, delete, list
"""
from fastapi import APIRouter
from psycopg2 import sql
import psycopg2
import os
from ...utils.dbConn import getConn
from ...utils import security

router = APIRouter(
    prefix='/database'
)

"""Creates a database with given name"""
@router.put('/create')
async def createDatabase(token:str, name:str):
    data = security.validateToken(token)

    if not security.validateRole(data['iss'], data['role'], 'put', 'system/database/create'):
        raise security.unauthorized

    with open('scripts/system/database/create.sql') as f:
        query = f.read()
        f.close()

    query = sql.SQL(query).format(DBName=sql.Identifier(name))

    try:
        conn = getConn('system')
        conn.autocommit=True
        with conn.cursor() as cur:
            cur.execute(query)
            cur.close()
        
        conn.autocommit=False
        conn.close()

        return {"message": "Operation Complete"}
    except Exception as e:
        print(e)
        raise security.something_wrong


"""Deletes a database"""
@router.delete('/delete')
async def deleteDatabase(token:str, name:str):
    data = security.validateToken(token)

    if not security.validateRole(data['iss'], data['role'], 'delete', 'system/database/delete'):
        raise security.unauthorized
    
    try:
        conn = getConn('system')
        conn.autocommit=True
        with open('scripts/system/database/delete.sql') as f:
            query = f.read()
            f.close()

        query = sql.SQL(query).format(DBName=sql.Identifier(name))

        with conn.cursor() as cur:
            cur.execute(query)
            cur.close()

        conn.autocommit=False
        conn.close()

        return {"message": "Operation Complete"}
    except:
        raise security.something_wrong


"""Lists databases on server"""
@router.get('/list')
async def listDatabases(token:str):
    data = security.validateToken(token)

    if not security.validateRole(data['iss'], data['role'], 'get', 'system/database/list'):
        raise security.unauthorized
    
    with open('scripts/system/database/list.sql') as f:
        query = f.read()
        f.close()

    try:
        conn = getConn('system')    
        
        with conn.cursor() as cur:
            cur.execute(query)
            res = cur.fetchall()
            cur.close()
        
        conn.close()
        
        return res
    except:
        raise security.something_wrong