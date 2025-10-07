from fastapi import FastAPI
from .routers.system import main as system
from .utils.dbConn import getConn
from .utils import security
from psycopg2 import sql

# App construction and routers
app = FastAPI()
app.include_router(system.router)

# Online check
@app.get('/')
async def root():
    return {"message": "Hello World!!"}

"""Creates system database"""
@app.put('/sysdb')
async def sysDb():
    conn = getConn('postgres')
    with open('scripts/system/database/create.sql') as f:
        query = f.read()
        f.close()

    with open('scripts/system/database/delete.sql') as f:
        query2 = f.read()
        f.close()

    query = sql.SQL(query).format(DBName=sql.Identifier("system"))
    query2 = sql.SQL(query2).format(DBName=sql.Identifier("postgres"))

    try:
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(query)
            res = "Created System Database"
            cur.close()
        conn.autocommit = False
        conn.close()
        conn = getConn('system')
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(query2)
            cur.close()
        conn.autocommit = False
        conn.close()
        return res
    except Exception as e:
        print(e)
        return security.something_wrong