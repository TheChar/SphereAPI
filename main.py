from fastapi import FastAPI, HTTPException, status
import psycopg2
import os
from passlib.context import CryptContext

app = FastAPI()

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

conn = psycopg2.connect(
    hostname=os.environ['DB_HOSTNAME'],
    dbname=os.environ['DB_NAME'],
    username=os.environ['DB_USERNAME'],
    password=os.environ['DB_PASSWORD'],
    port=os.environ['DB_PORT']
)

"""Root route returns hello world"""
@app.get('/')
async def root():
    return {"message": "Hello World!!"}

"""Login route to assign JWT to client"""
@app.get('/login')
async def login(username: str, password: str):
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
    
    #get a new token and give to user

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
