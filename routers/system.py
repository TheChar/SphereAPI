from fastapi import APIRouter, HTTPException, status
from ..utils.dbConn import getConn
from ..utils import security
import os
from passlib.context import CryptContext

router = APIRouter(
    prefix='/system'
)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

roles = [
    ['put', 'system/user/add', "Adds a user to the system"],
    ['put', 'system/role/add', "Adds a role to the system if the corresponding SQL file exists"],
    ['delete', 'system/role/delete', "Deletes a role from the system"],
    ['get', 'system/role/get', "Gets the roles associated with a given username"],
    ['get', 'system/user/get', "Gets user information associated with a username"],
    ['get', 'system/user/getAll', "Gets all information about all users"],
    ['put', 'system/role/bind', "Binds a role to a user with a given username, operation, and route"],
    ['delete', 'system/role/unbind', "Unbinds role from user"],
]


"""Initializes the system databases. Needs security foundation support

"""
@router.put('/initialize')
async def initialize():
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="This route does not exist"
    )
    conn = getConn('system')
    with open('scripts/system/createStructure.sql') as f:
        query = f.read()
        f.close()

    with conn.cursor() as cur:
        cur.execute(query)
        res1 = cur.fetchall()
        cur.close()

    with open('scripts/system/user/add.sql') as f:
        query = f.read()
        f.close()

    params = {
        "username": "admin",
        "hashedpassword": pwd_context.hash('password'),
        "expmins": 30
    }

    with conn.cursor() as cur:
        cur.execute(query, params)
        res2 = cur.fetchone()
        cur.close()

    #Add role bindings for admin ==============================================================================================

    with open('scripts/system/role/bind.sql') as f:
        query = f.read()
        f.close()

    for role in roles:
        params = {
            "username": "admin",
            "operation": role[0],
            "route": role[1]
        }

        with conn.cursor() as cur:
            cur.execute(query, params)
            cur.close()

    conn.commit()

    conn.close()

    return (res1, res2)


"""Adds a user to the system

Returns:
    json: UserID and Username
"""
@router.put('/user/add')
async def addUser(token: str, username:str, password:str):
    data = security.validateToken(token)

    #implement role protections here
    if not security.validateRole(data['sub'], 'put', 'system/user/add'):
        raise security.unauthorized
    
    conn = getConn('system')

    params = {
        "username": username,
        "hashedpassword": pwd_context.hash(password),
        "expmins": 30
    }

    with open('scripts/system/user/add.sql') as f:
        query = f.read()
        f.close()

    with conn.cursor() as cur:
        cur.execute(query, params)
        res = cur.fetchall()
        cur.close()

    conn.commit()

    conn.close()

    return res


"""Adds a role to the system

"""
@router.put('/role/add')
async def addRole(token:str, operation: str, route: str):
    data = security.validateToken(token)
    
    if not security.validateRole(data['sub'], 'put', 'system/role/add'):
        raise security.unauthorized

    operations = ["get", "put", "post", "delete"]

    if operation.lower() not in operations:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Operation must be get, put, post, or delete"
        )
    
    if not os.path.isdir(f'scripts/{route}'):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'{route} does not exist'
        )
    
    conn = getConn('system')

    params = {
        "operation": operation,
        "route": route
    }

    with open('scripts/system/role/add.sql') as f:
        query = f.read()
        f.close()

    with conn.cursor() as cur:
        cur.execute(query, params)
        res = cur.fetchall()
        cur.close()

    conn.commit()

    conn.close()

    return res

@router.delete('/role/delete')
async def deleteRole(token:str, operation:str, route:str):
    data = security.validateToken(token)

    if not security.validateRole(data['sub'], 'delete', 'system/role/delete'):
        raise security.unauthorized
    
    with open('scripts/system/role/delete.sql') as f:
        query = f.read()
        f.close()

    params = {
        "operation": operation,
        "route": route
    }

    conn = getConn('system')

    with conn.cursor() as cur:
        cur.execute(query, params)
        res = cur.fetchall()
        cur.close()

    conn.commit()
    conn.close()

    return res

@router.get('/role/get')
async def getRoles(token:str, username:str):
    data = security.validateToken(token)

    if not security.validateRole(data['sub'], 'get', 'system/role/get'):
        raise security.unauthorized
    
    # Applications can only access their own roles except admin
    if data['sub'] != 'admin' and username != data['sub']:
        raise security.unauthorized
    
    with open('scripts/system/role/getByUsername.sql') as f:
        query = f.read()
        f.close()

    conn = getConn('system')

    params = {
        "username": username
    }

    with conn.cursor() as cur:
        cur.execute(query, params)
        res = cur.fetchall()
        cur.close()

    conn.close()

    return res

"""Gets user information from the user with given username"""
@router.get('/user/get')
async def getUser(token:str, username:str):
    data = security.validateToken(token)
    
    #Implement role protections here
    if not security.validateRole(data['sub'], 'get', 'system/user/get'):
        raise security.unauthorized

    with open('scripts/system/user/getByUsername.sql') as f:
        query = f.read()
        f.close()

    params = {
        "username": username
    }

    conn = getConn('system')

    with conn.cursor() as cur:
        cur.execute(query, params)
        res = cur.fetchone()
        cur.close()

    conn.close()

    return res

@router.get('/user/getAll')
async def getUsers(token:str):
    data = security.validateToken(token)

    if not security.validateRole(data['sub'], 'get', 'system/user/getAll'):
        raise security.unauthorized

    with open('scripts/system/user/getAll.sql') as f:
        query = f.read()
        f.close()
    
    conn = getConn('system')

    with conn.cursor() as cur:
        cur.execute(query)
        res = cur.fetchall()
        cur.close()

    conn.close()

    return res

@router.put('/role/bind')
async def bindRole(token:str, username:str, operation:str, route:str):
    data = security.validateToken(token)

    if not security.validateRole(data['sub'], 'put', 'system/role/bind'):
        raise security.unauthorized

    params = {
        "username": username,
        "route": route,
        "operation": operation
    }

    with open('scripts/system/role/bind.sql') as f:
        query = f.read()
        f.close()

    conn = getConn('system')

    with conn.cursor() as cur:
        cur.execute(query, params)
        res = cur.fetchone()
        cur.close()

    conn.commit()
    conn.close()

    return res

@router.delete('/role/unbind')
async def unbindRole(token:str, username:str, route:str, operation:str):
    data = security.validateToken(token)

    if not security.validateRole(data['sub'], 'delete', 'system/role/unbind'):
        raise security.unauthorized
    
    if username == 'admin':
        raise security.admin_infringement
    
    with open('scripts/system/role/unbind.sql') as f:
        query = f.read()
        f.close()

    conn = getConn('system')

    params = {
        "username": username,
        "route": route,
        "operation": operation
    }

    with conn.cursor() as cur:
        cur.execute(query, params)
        res = cur.fetchall()
        cur.close()
    
    conn.commit()
    conn.close()

    return {"remaining roles": res}

@router.get('/help')
async def help():
    res = ""
    for role in roles:
        res += f"Route: {role[1]} => {role[2]}\n"
    return res

"""Token generating endpoint"""
@router.get('/token/get')
async def getToken(username:str, password:str):
    params = {
        "username": username,
    }

    with open('scripts/system/user/getByUsername.sql') as f:
        query = f.read()
        f.close()

    conn = getConn('system')

    with conn.cursor() as cur:
        cur.execute(query, params)
        res = cur.fetchone()
        cur.close()

    conn.close()

    #Bad username
    if res == None:
        raise security.bad_credentials
    
    #Bad password
    if not pwd_context.verify(password, res[2]):
        raise security.bad_credentials
    
    token = security.generateToken(res[1], res[3], res[4])

    return token