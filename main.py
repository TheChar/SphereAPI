from fastapi import FastAPI, HTTPException, status
import psycopg2
import os
from datetime import datetime as dt
from datetime import timedelta
from passlib.context import CryptContext
import jwt
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

conn = psycopg2.connect(
    hostname=os.getenv('DB_HOSTNAME'),
    dbname=os.getenv('DB_NAME'),
    username=os.getenv('DB_USERNAME'),
    password=os.getenv('DB_PASSWORD'),
    port=os.getenv('DB_PORT')
)

"""Root route returns hello world"""
@app.get('/')
async def root():
    return {"message": "Hello World!!"}

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
