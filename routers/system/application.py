"""
Routes: system/application/* => list, get, add, delete
"""

from fastapi import APIRouter
from ...utils import security
from ...utils.dbConn import getConn

router = APIRouter(prefix='/application')

db = 'system'

"""List all applications in system"""
@router.get('/list')
async def listApplications(token:str):
    data = security.validateToken(token)
    if not security.validateRole(data['iss'], data['role'], 'get', 'system/application/list'):
        raise security.unauthorized
    
    with open('scripts/system/application/list.sql') as f:
        query = f.read()
        f.close()
    
    try:
        conn = getConn(db)
        with conn.cursor() as cur:
            cur.execute(query)
            res = cur.fetchall()
            cur.close()
        conn.close()
        return res
    except Exception as e:
        print(e)
        raise security.something_wrong
    
"""Get all info about an application"""
@router.get('/get')
async def getApplication(token:str, title:str):
    data = security.validateToken(token)
    if not security.validateRole(data['iss'], data['role'], 'get', 'system/application/get'):
        raise security.unauthorized
    
    with open('scripts/system/application/get.sql') as f:
        query = f.read()
        f.close()

    params = {
        "Title": title
    }
    
    try:
        conn = getConn(db)
        with conn.cursor() as cur:
            cur.execute(query, params)
            res = cur.fetchone()
            cur.close()
        conn.close()
        return res
    except Exception as e:
        print(e)
        raise security.something_wrong
    
"""Add a new application to the system"""
@router.put('/add')
async def addApplication(token:str, title:str):
    data = security.validateToken(token)
    if not security.validateRole(data['iss'], data['role'], 'put', 'system/application/add'):
        raise security.unauthorized
    
    with open('scripts/system/application/add.sql') as f:
        query = f.read()
        f.close()

    params = {
        "Title": title
    }

    #TODO when role handling is done, add new app initialize endpoint to the system admin role
    
    try:
        conn = getConn(db)
        with conn.cursor() as cur:
            cur.execute(query, params)
            res = cur.fetchone()
            cur.close()
        conn.commit()
        conn.close()
        return res
    except Exception as e:
        print(e)
        raise security.something_wrong
    
"""Delete an application, its roles, and cleans unused routes after deletion"""
@router.delete('/delete')
async def deleteApplication(token:str, title:str):
    data = security.validateToken(token)
    if not security.validateRole(data['iss'], data['role'], 'delete', 'system/application/delete'):
        raise security.unauthorized
    
    with open('scripts/system/application/delete.sql') as f:
        query = f.read()
        f.close()

    params = {
        "Title": title
    }
    
    try:
        conn = getConn(db)
        with conn.cursor() as cur:
            cur.execute(query, params)
            res = "Operation Successful"
            cur.close()
        conn.commit()
        conn.close()
        return res
    except Exception as e:
        print(e)
        raise security.something_wrong