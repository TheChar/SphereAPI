"""
Routes: /system/user/* => add, changePassword, changeName, changeExpMins, delete, list/all, list/app, list/role, register/app, register/role
"""

from fastapi import APIRouter
from ...utils import security
from ...utils.dbConn import getConn
from datetime import datetime as dt
from passlib.context import CryptContext

router = APIRouter(prefix='/user')
db = 'system'
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

"""Add new user, registering them automatically to the System application with basic priveleges"""
@router.put('/add')
async def addUser(token:str, username:str, password:str, name:str):
    data = security.validateToken(token)
    if not security.validateRole(data['iss'], data['role'], 'put', 'system/user/add'):
        raise security.unauthorized
    
    with open('scripts/system/user/add.sql') as f:
        query = f.read()
        f.close()

    params = {
        "Username": username,
        "HashedPassword": pwd_context.encrypt(password),
        "Name": name,
        "ExpMins": 60,
        "JoinDate": dt.now()
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

"""Changes user password"""
@router.post('/changePassword')
async def changePassword(token:str, oldpass:str, newpass:str):
    data = security.validateToken(token)
    if not security.validateRole(data['iss'], data['role'], 'post', 'system/user/changePassword'):
        raise security.unauthorized
    
    with open('scripts/system/user/getby/username.sql') as f:
        query = f.read()
        f.close()

    with open('scripts/system/user/changePassword.sql') as f:
        query2 = f.read()
        f.close()

    params = {
        "Username": data['sub'],
        "HashedPassword": pwd_context.hash(newpass)
    }
    
    try:
        conn = getConn(db)
        with conn.cursor() as cur:
            cur.execute(query, params)
            res = cur.fetchone()
            cur.close()
        if not pwd_context.verify(oldpass, res[2]):
            raise security.unauthorized
        with conn.cursor() as cur:
            cur.execute(query2, params)
            res = {"detail": "Operation Successful"}
            cur.close()
        conn.commit()
        conn.close()
        return res
    except Exception as e:
        print(e)
        raise security.something_wrong

"""Changes user name"""
@router.post('/changeName')
async def changeName(token:str, name:str):
    data = security.validateToken(token)
    if not security.validateRole(data['iss'], data['role'], 'post', 'system/user/changeName'):
        raise security.unauthorized
    
    with open('scripts/system/user/changeName.sql') as f:
        query = f.read()
        f.close()

    params = {
        "Username": data['sub'],
        "Name": name
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
    
"""Changes expiry minutes on user token"""
@router.post('/changeExpiration')
async def changeExpiration(token:str, username:str, minutes:str):
    data = security.validateToken(token)
    if not security.validateRole(data['iss'], data['role'], 'post', 'system/user/changeExpiration'):
        raise security.unauthorized
    
    with open('scripts/system/user/changeExpiration.sql') as f:
        query = f.read()
        f.close()

    params = {
        "Username": username,
        "ExpMins": minutes
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
    
"""Deletes user if they aren't registered outside of System"""
@router.delete('/delete')
async def deleteUser(token:str, username:str):
    data = security.validateToken(token)
    if not security.validateRole(data['iss'], data['role'], 'delete', 'system/user/delete'):
        raise security.unauthorized
    
    with open('scripts/system/user/delete.sql') as f:
        query = f.read()
        f.close()

    params = {
        "Username": username,
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
    
"""Registers a user for an app - automatically putting them in the given role for the app"""
@router.put('/register/app')
async def registerOnApp(token:str, appTitle:str, roleTitle:str, appData:str, username:str):
    data = security.validateToken(token)
    if not security.validateRole(data['iss'], data['role'], 'put', 'system/user/register/app'):
        raise security.unauthorized
    
    with open('scripts/system/user/register/app.sql') as f:
        query = f.read()
        f.close()

    params = {
        "AppTitle": appTitle,
        "Username": username,
        "RoleTitle": roleTitle,
        "JoinDate": dt.now(),
        "Data": appData
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
    
"""Removes a user from an app"""
@router.delete('/register/leaveApp')
async def registerOnApp(token:str, appTitle:str, username:str):
    data = security.validateToken(token)
    if not security.validateRole(data['iss'], data['role'], 'delete', 'system/user/register/leaveApp'):
        raise security.unauthorized
    
    with open('scripts/system/user/register/leaveApp.sql') as f:
        query = f.read()
        f.close()

    params = {
        "AppTitle": appTitle,
        "Username": username,
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
    
"""Sets a role for the user within the given app"""
@router.put('/register/role')
async def registerOnApp(token:str, appTitle:str, roleTitle:str, username:str):
    data = security.validateToken(token)
    if not security.validateRole(data['iss'], data['role'], 'put', 'system/user/register/role'):
        raise security.unauthorized
    
    with open('scripts/system/user/register/role.sql') as f:
        query = f.read()
        f.close()

    with open('scripts/system/role/get.sql') as f:
        query2 = f.read()
        f.close()

    params = {
        "AppTitle": appTitle,
        "Username": username,
        "RoleTitle": roleTitle
    }
    
    try:
        conn = getConn(db)
        with conn.cursor() as cur:
            cur.execute(query2, params)
            res = cur.fetchone()
            cur.close()
        if res == None:
            raise Exception('That role doesn\'t exist')
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
    
"""Lists all users registered to an app"""
@router.get('/list/app')
async def listAppUsers(token:str, appTitle:str):
    data = security.validateToken(token)
    if not security.validateRole(data['iss'], data['role'], 'get', 'system/user/list/app'):
        raise security.unauthorized
    
    with open('scripts/system/user/list/app.sql') as f:
        query = f.read()
        f.close()

    params = {
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
    
"""Lists all users with the given role in an app"""
@router.get('/list/role')
async def listAllUsers(token:str, appTitle:str, roleTitle:str):
    data = security.validateToken(token)
    if not security.validateRole(data['iss'], data['role'], 'get', 'system/user/list/role'):
        raise security.unauthorized
    
    with open('scripts/system/user/list/role.sql') as f:
        query = f.read()
        f.close()

    params = {
        "AppTitle": appTitle,
        "RoleTitle": roleTitle
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
    
"""Lists all users"""
@router.get('/list/all')
async def listAllUsers(token:str):
    data = security.validateToken(token)
    if not security.validateRole(data['iss'], data['role'], 'get', 'system/user/list/all'):
        raise security.unauthorized
    
    with open('scripts/system/user/list/all.sql') as f:
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