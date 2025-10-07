"""
Routes: system/role/* => list, get, add, update, delete, route/list, route/bind, route/delete, route/unbind
"""

from fastapi import APIRouter
from ...utils import security
from ...utils.dbConn import getConn

router = APIRouter(prefix='/role')
db = 'system'

"""List roles for an application"""
@router.get('/list')
async def listRoles(token:str, appTitle:str):
    data = security.validateToken(token)
    if not security.validateRole(data['iss'], data['role'], 'get', 'system/role/list'):
        raise security.unauthorized
    
    with open('scripts/system/role/list.sql') as f:
        query = f.read()
        f.close()

    params = {
        "Title": appTitle
    }
    
    try:
        conn = getConn(db)
        with conn.cursor() as cur:
            cur.execute(query, params)
            res = cur.fetchall()
            cur.close()
        conn.close()
        return res
    except Exception as e:
        print(e)
        raise security.something_wrong
    
"""Get role for an application"""
@router.get('/get')
async def getRole(token:str, roleTitle:str, appTitle:str):
    data = security.validateToken(token)
    if not security.validateRole(data['iss'], data['role'], 'get', 'system/role/get'):
        raise security.unauthorized
    
    with open('scripts/system/role/get.sql') as f:
        query = f.read()
        f.close()

    params = {
        "RoleTitle": roleTitle,
        "AppTitle": appTitle
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
    
"""Add role for an application"""
@router.put('/add')
async def addRole(token:str, roleTitle:str, description:str, appTitle:str):
    data = security.validateToken(token)
    if not security.validateRole(data['iss'], data['role'], 'put', 'system/role/add'):
        raise security.unauthorized
    
    with open('scripts/system/role/add.sql') as f:
        query = f.read()
        f.close()

    params = {
        "Title": roleTitle,
        "Description": description,
        "AppTitle": appTitle
    }
    
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
    
"""Update a roles description"""
@router.post('/update')
async def updateRole(token:str, roleTitle:str, description:str, appTitle:str):
    data = security.validateToken(token)
    if not security.validateRole(data['iss'], data['role'], 'post', 'system/role/update'):
        raise security.unauthorized
    
    with open('scripts/system/role/update.sql') as f:
        query = f.read()
        f.close()

    params = {
        "RoleTitle": roleTitle,
        "Description": description,
        "AppTitle": appTitle
    }
    
    try:
        conn = getConn(db)
        with conn.cursor() as cur:
            cur.execute(query, params)
            cur.close()
        conn.commit()
        conn.close()
        return "Success"
    except Exception as e:
        print(e)
        raise security.something_wrong
    
"""Delete a role given no user has it and it isn't the last role for the application"""
@router.delete('/delete')
async def deleteRole(token:str, roleTitle:str, appTitle:str):
    data = security.validateToken(token)
    if not security.validateRole(data['iss'], data['role'], 'delete', 'system/role/delete'):
        raise security.unauthorized
    
    with open('scripts/system/role/delete.sql') as f:
        query = f.read()
        f.close()

    params = {
        "RoleTitle": roleTitle,
        "AppTitle": appTitle
    }
    
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
    
"""Lists all the routes associated with a given role in an application"""
@router.get('/route/list')
async def listRoutes(token:str, roleTitle:str, appTitle:str):
    data = security.validateToken(token)
    if not security.validateRole(data['iss'], data['role'], 'get', 'system/role/route/list'):
        raise security.unauthorized
    
    with open('scripts/system/role/route/list.sql') as f:
        query = f.read()
        f.close()

    params = {
        "RoleTitle": roleTitle,
        "AppTitle": appTitle
    }
    
    try:
        conn = getConn(db)
        with conn.cursor() as cur:
            cur.execute(query, params)
            res = cur.fetchall()
            cur.close()
        conn.close()
        return res
    except Exception as e:
        print(e)
        raise security.something_wrong

"""Binds a new route to a given role in a given application"""
@router.put('/route/bind')
async def bindRoute(token:str, roleTitle:str, appTitle:str, operation:str, routeName:str):
    data = security.validateToken(token)
    if not security.validateRole(data['iss'], data['role'], 'put', 'system/role/route/bind'):
        raise security.unauthorized
    
    with open('scripts/system/role/route/bind.sql') as f:
        query = f.read()
        f.close()

    params = {
        "RoleTitle": roleTitle,
        "AppTitle": appTitle,
        "Operation": operation,
        "RouteName": routeName
    }
    
    try:
        conn = getConn(db)
        with conn.cursor() as cur:
            cur.execute(query, params)
            res = {"detail": "Operation Successful"}
            cur.close()
        conn.commit()
        conn.close()
        return res
    except Exception as e:
        print(e)
        raise security.something_wrong

"""Deletes a route, raising an error if route is in use"""
@router.delete('/route/delete')
async def deleteRoute(token:str, operation:str, routeName:str):
    data = security.validateToken(token)
    if not security.validateRole(data['iss'], data['role'], 'delete', 'system/role/route/delete'):
        raise security.unauthorized
    
    with open('scripts/system/role/route/delete.sql') as f:
        query = f.read()
        f.close()

    params = {
        "Operation": operation,
        "RouteName": routeName
    }
    
    try:
        conn = getConn(db)
        with conn.cursor() as cur:
            cur.execute(query, params)
            res = {"detail": "Operation Successful"}
            cur.close()
        conn.commit()
        conn.close()
        return res
    except Exception as e:
        print(e)
        raise security.something_wrong
    
"""Unbinds a specific route from a role given the binding exists."""
@router.delete('/route/unbind')
async def unbindRoute(token:str, roleTitle:str, appTitle:str, operation:str, routeName:str):
    data = security.validateToken(token)
    if not security.validateRole(data['iss'], data['role'], 'delete', 'system/role/route/unbind'):
        raise security.unauthorized
    
    with open('scripts/system/role/route/unbind.sql') as f:
        query = f.read()
        f.close()

    params = {
        "RoleTitle": roleTitle,
        "AppTitle": appTitle,
        "Operation": operation,
        "RouteName": routeName
    }
    
    try:
        conn = getConn(db)
        with conn.cursor() as cur:
            cur.execute(query, params)
            res = {"detail": "Operation Successful"}
            cur.close()
        conn.commit()
        conn.close()
        return res
    except Exception as e:
        print(e)
        raise security.something_wrong