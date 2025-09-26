from typing import Literal
from fastapi import APIRouter, HTTPException, status
from ..dbConn import getConn
import os
from datetime import datetime as dt
from datetime import timedelta
import jwt
import psycopg2
from passlib.context import CryptContext

router = APIRouter(
    prefix='/system'
)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


"""Initializes the system databases. Needs security foundation support

"""
@router.put('/initialize')
async def initialize():
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Secure method not implemented"
    )
    conn = getConn('system')
    with open('scripts/system/createStructure.sql') as f:
        query = f.read()

    with conn.cursor() as cur:
        cur.execute(query)
        res = cur.fetchall()

    conn.commit()

    conn.close()

    return res


"""Adds a user to the system

Returns:
    json: UserID and Username
"""
@router.put('/addUser')
async def addUser(username:str, password:str):
    conn = getConn('system')

    params = {
        "username": username,
        "hashedpassword": pwd_context.hash(password)
    }

    with open('scripts/system/addUser.sql') as f:
        query = f.read()

    with conn.cursor() as cur:
        cur.execute(query, params)
        res = cur.fetchall()

    conn.commit()

    conn.close()

    return res


"""Adds a role to the system

"""
@router.put('/addRole')
async def addRole(operation: str, route: str):
    operations = ["get", "put", "post", "delete"]

    if operation.lower() not in operations:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Operation must be get, put, post, or delete"
        )
    
    if not os.path.isdir(f'scripts/{route}'):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'{route.capitalize} does not exist'
        )
    
    conn = getConn('system')

    params = {
        "operation": operation,
        "route": route
    }

    with open('scripts/system/addRole.sql') as f:
        query = f.read()

    with conn.cursor() as cur:
        cur.execute(query, params)
        res = cur.fetchall()

    conn.commit()

    conn.close()

    return res

"""Gets user information from the user with given username"""
@router.get('/getUser')
async def getUser(username:str):
    with open('scripts/system/getUser.sql') as f:
        query = f.read()

    params = {
        "username": username
    }

    conn = getConn('system')

    with conn.cursor() as cur:
        cur.execute(query, params)
        res = cur.fetchall()

    conn.close()

    return res


@router.get('/getToken')
async def getToken(username:str, password:str):
    params = {
        "username": username,
    }

    with open('scripts/system/getUser.sql') as f:
        query = f.read()

    conn = getConn('system')

    with conn.cursor() as cur:
        cur.execute(query, params)
        res = cur.fetchone()

    conn.close()

    #Add use case for username that doesn't exist here
    if res == None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Credentials"
        )
    
    if not pwd_context.verify(password, res[2]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Credentials"
        )
    
    #Get users roles and insert
    
    data = {
        "iss": "SphereAPI",
        "sub": username,
        "exp": dt.now() + timedelta(minutes=30),
        "iat": dt.now(),
        "roles": []
    }
    
    token = jwt.encode(data, os.getenv('SECRET'), os.getenv('ALGORITHM'))

    return token