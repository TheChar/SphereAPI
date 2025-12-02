from fastapi import APIRouter, HTTPException, status
from ..system import application, database, role, user
from ...utils.dbConn import getConn
from ...utils import security
from passlib.context import CryptContext
from datetime import datetime as dt, timezone

router = APIRouter(
    prefix='/system'
)

router.include_router(application.router)
router.include_router(database.router)
router.include_router(role.router)
router.include_router(user.router)

db = 'system'
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

@router.put('/initialize')
async def initialize():
    # raise HTTPException(
    #     status_code=status.HTTP_403_FORBIDDEN,
    #     detail="This route does not exist"
    # )
    conn = getConn(db)
    with open('scripts/system/initialize.sql') as f:
        query = f.read()
        f.close()

    with conn.cursor() as cur:
        cur.execute(query)
        res1 = cur.fetchall()
        cur.close()

    #Add the "System application"
    with open('scripts/system/application/add.sql') as f:
        query2 = f.read()
        f.close()

    params2 = {
        "Title": "System"
    }
    
    with conn.cursor() as cur:
        cur.execute(query2, params2)
        res2 = cur.fetchone()
        cur.close()
    
    #Define roles for system
    with open('scripts/system/role/add.sql') as f:
        query3 = f.read()
        f.close()
    
    params3 = {
        "Title": "Default",
        "Description": "The default user account",
        "AppTitle": "System"
    }

    with conn.cursor() as cur:
        cur.execute(query3, params3)
        cur.close()
    
    params3 = {
        "Title": "Admin",
        "Description": "The administrative account",
        "AppTitle": "System"
    }

    with conn.cursor() as cur:
        cur.execute(query3, params3)
        cur.close()

    #Add routes for the roles
    default_routes = [
        ('post', 'system/user/changeName'),
        ('post', 'system/user/changePassword'),
    ]

    admin_routes = [
        ('get', 'system/application/list'),
        ('get', 'system/application/get'),
        ('put', 'system/application/add'),
        ('delete', 'system/application/delete'),
        ('put', 'system/database/create'),
        ('get', 'system/database/list'),
        ('delete', 'system/database/delete'),
        ('get', 'system/role/list'),
        ('get', 'system/role/get'),
        ('put', 'system/role/add'),
        ('post', 'system/role/update'),
        ('delete', 'system/role/delete'),
        ('get', 'system/role/route/list'),
        ('put', 'system/role/route/bind'),
        ('delete', 'system/role/route/delete'),
        ('delete', 'system/role/route/unbind'),
        ('put', 'system/user/add'),
        ('post', 'system/user/changeExpiration'),
        ('delete', 'system/user/delete'),
        ('put', 'system/user/register/app'),
        ('delete', 'system/user/register/leaveApp'),
        ('put', 'system/user/register/role'),
        ('get', 'system/user/list/app'),
        ('get', 'system/user/list/role'),
        ('get', 'system/user/list/all')
    ]

    with open('scripts/system/role/route/bind.sql') as f:
        query4 = f.read()
        f.close()

    for operation, route in default_routes:
        params4 = {
            "RoleTitle": "Default",
            "AppTitle": "System",
            "Operation": operation,
            "RouteName": route
        }

        with conn.cursor() as cur:
            cur.execute(query4, params4)
            cur.close()

    for operation, route in default_routes:
        params4 = {
            "RoleTitle": "Admin",
            "AppTitle": "System",
            "Operation": operation,
            "RouteName": route
        }

        with conn.cursor() as cur:
            cur.execute(query4, params4)
            cur.close()

    for operation, route in admin_routes:
        params4 = {
            "RoleTitle": "Admin",
            "AppTitle": "System",
            "Operation": operation,
            "RouteName": route
        }

        with conn.cursor() as cur:
            cur.execute(query4, params4)
            cur.close()
    
    #Add the admin account
    with open('scripts/system/user/add.sql') as f:
        query5 = f.read()
        f.close()

    params5 = {
        "Username": "admin",
        "HashedPassword": pwd_context.hash('password'),
        "Name": "Admin",
        "ExpMins": 120,
        "JoinDate": dt.now(timezone.utc)
    }

    with conn.cursor() as cur:
        cur.execute(query5, params5)
        res5 = cur.fetchone()
        cur.close()

    #Promote admin to Admin

    with open('scripts/system/user/register/role.sql') as f:
        query6 = f.read()
        f.close()

    params6 = {
        "Username": "admin",
        "RoleTitle": "Admin",
        "AppTitle": "System"
    }

    with conn.cursor() as cur:
        cur.execute(query6, params6)
        cur.close()

    conn.commit()

    conn.close()

    return {"detail": "Operation Successful"}

"""Token generating endpoint"""
@router.post('/token')
async def getToken(username:str, password:str, appTitle:str):
    params = {
        "Username": username,
        "AppTitle": appTitle
    }

    with open('scripts/system/user/getby/userapp.sql') as f:
        query = f.read()
        f.close()

    try:

        conn = getConn(db)

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
        
        token = security.generateToken(res[1], res[3], res[4][0], appTitle, res[5])

        return token
    except Exception as e:
        print(e)
        raise security.something_wrong