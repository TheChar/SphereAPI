from fastapi import FastAPI, HTTPException, status
import psycopg2
from psycopg2 import sql
import os
from datetime import datetime as dt
from datetime import timedelta
from passlib.context import CryptContext
import jwt
from dotenv import load_dotenv
from .routers import test

load_dotenv()

app = FastAPI()
app.include_router(test.router)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

conn = psycopg2.connect(
    host=os.getenv('DB_HOSTNAME'),
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USERNAME'),
    password=os.getenv('DB_PASSWORD'),
    port=os.getenv('DB_PORT')
)

@app.get('/flushpg')
async def flush(dbname:str):
    conn.autocommit = True

    with open('scripts/dropDatabase.sql') as f:
        query = f.read()
        f.close()

    query = sql.SQL(query).format(sql.Identifier(dbname))

    with conn.cursor() as cur:
        cur.execute(query)
    conn.autocommit = False

@app.get('/initializeAPI')
async def initAPI():
    #create database here
    conn.autocommit = True
    params = {
        "dbname": "api_system"
    }
    with open('scripts/createDatabase.sql') as f:
        sql = f.read()
        f.close()
    
    with conn.cursor() as cur:
        cur.execute(sql, params)
    conn.autocommit = False

    with open('scripts/system/createStructure.sql') as f:
        sql = f.read()

    with conn.cursor() as cur:
        cur.execute(sql)
        res = cur.fetchall()

    return res

"""Login route to assign JWT to client"""
@app.get('/getToken')
async def getToken(username: str, password: str):
    params = {
        'username': username
    }

    with open('scripts/system/getUser.sql') as f:
        sql = f.read()

    with conn.cursor() as cur:
        cur.execute(sql, params)
        res = cur.fetchall()
        cur.close()

    print(res) #if user not in db, need to raise exception
    
    if not pwd_context.verify(password, res['HashedPassword']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    data = {
        "sub": username,
        "exp": dt.now() + timedelta(minutes=os.getenv('EXPIRE_IN_MIN'))
    }
    token = jwt.encode(data, os.getenv('SECRET'), os.getenv('ALGORITHM'))

"""Route to create a new user (for future clients)"""
@app.post('/createUser')
async def createUser(username: str, password: str, type: str):
    
    hashedPass = pwd_context.hash(password)

    params = {
        'username': username,
        'hashedpassword': hashedPass,
        'type': type
    }

    with open('/scripts/system/addUser.sql') as f:
        sql = f.read()
    
    with conn.cursor() as cur:
        cur.execute(sql, params)
        res = cur.fetchall()
        cur.close()

    return res
