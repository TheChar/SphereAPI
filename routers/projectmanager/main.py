from fastapi import APIRouter
from ...utils.dbConn import getConn
from ...utils import security
from .contributor import router as contributor
from .organization import router as organization
from .project import router as project
from .tag import router as tag
from .timeentry import router as timeentry

router = APIRouter(prefix='/projectmanager')
db = 'projectmanager'
app = "Project Manager"

router.include_router(contributor)
router.include_router(organization)
router.include_router(project)
router.include_router(tag)
router.include_router(timeentry)

@router.get('/')
async def onlineCheck():
    return "Project Manager API is online"

@router.put('/initialize')
async def initialize(token:str):
    data = security.validateToken(token)
    if not security.validateRole('System', data['role'], 'put', 'projectmanager/initialize'):
        raise security.unauthorized
    conn = getConn(db)
    with open('scripts/projectmanager/initialize.sql') as f:
        query = f.read()
        f.close()

    with conn.cursor() as cur:
        cur.execute(query)
        cur.close()

    conn.commit()
    conn.close()
    conn = getConn('system')

    #Add the "Project Manager" application
    with open('scripts/system/application/add.sql') as f:
        query2 = f.read()
        f.close()

    params2 = {
        "Title": "Project Manager"
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
        "AppTitle": "Project Manager"
    }

    with conn.cursor() as cur:
        cur.execute(query3, params3)
        cur.close()

    #Add routes for the roles
    default_routes = [
        #All routes need to go here as ('operation', 'route')
        ('put', 'projectmanager/contributor/register'),
        ('delete', 'projectmanager/contributor/leave'),
        ('put', 'projectmanager/contributor/organization/join'),
        ('delete', 'projectmanager/contributor/organization/leave'),
        ('get', 'projectmanager/contributor/organization/list'),
        ('put', 'projectmanager/organization/create'),
        ('delete', 'projectmanager/organization/dissolve'),
        ('post', 'projectmanager/organization/transfer'),
        ('put', 'projectmanager/organization/invite'),
        ('put', 'projectmanager/project/create'),
        ('post', 'projectmanager/project/update'),
        ('delete', 'projectmanager/project/delete'),
        ('get', 'projectmanager/project/get'),
        ('post', 'projectmanager/project/transfer'),
        ('get', 'projectmanager/project/list/all'),
        ('get', 'projectmanager/project/list/byowner'),
        ('get', 'projectmanager/project/list/bytag'),
        ('put', 'projectmanager/project/contributor/add'),
        ('post', 'projectmanager/project/contributor/remove'),
        ('post', 'projectmanager/project/contributor/restore'),
        ('put', 'projectmanager/project/tag/bind'),
        ('put', 'projectmanager/timeentry/create'),
        ('post', 'projectmanager/timeentry/update'),
        ('delete', 'projectmanager/timeentry/delete'),
        ('get', 'projectmanager/timeentry/list/byproject'),
        ('get', 'projectmanager/timeentry/list/bycontributor'),
        ('put', 'projectmanager/tag/create'),
        ('post', 'projectmanager/tag/update'),
        ('post', 'projectmanager/tag/transfer'),
        ('get', 'projectmanager/tag/list/byowner'),
        ('get', 'projectmanager/tag/list/byproject'),
        ('get', 'projectmanager/tag/get'),
        ('get', 'projectmanager/tag/project/get')
    ]

    with open('scripts/system/role/route/bind.sql') as f:
        query4 = f.read()
        f.close()

    for operation, route in default_routes:
        params4 = {
            "RoleTitle": "Default",
            "AppTitle": "Project Manager",
            "Operation": operation,
            "RouteName": route
        }

        with conn.cursor() as cur:
            cur.execute(query4, params4)
            cur.close()

    #Register contributor join routes to system roles
    with open('scripts/system/role/route/bind.sql') as f:
        query5 = f.read()
        f.close()

    roles = [
        'Admin',
        'Default'
    ]

    for role in roles:
        params5 = {
            "RoleTitle": role,
            "AppTitle": "System",
            "Operation": 'put',
            "RouteName": 'projectmanager/contributor/register'
        }

        with conn.cursor() as cur:
            cur.execute(query5, params5)
            cur.close()

    conn.commit()
    conn.close()

    return {"detail": "Operation Successful"}

"""For debugging"""
@router.delete('/destruct')
async def destructPM(token:str):
    data = security.validateToken(token)
    if not security.validateRole('System', data['role'], 'delete', 'projectmanager/destruct'):
        raise security.unauthorized
    with open('scripts/projectmanager/destruct.sql') as f:
        query = f.read()
        f.close()
    with open('scripts/system/application/delete.sql') as f:
        query2 = f.read()
        f.close()
    params = {
        "Title": app
    }
    try:
        conn = getConn(db)
        with conn.cursor() as cur:
            cur.execute(query)
            cur.close()
        conn.commit()
        conn.close()
        conn = getConn('system')
        with conn.cursor() as cur:
            cur.execute(query2, params)
            cur.close()
        conn.commit()
        conn.close()
        res = "Success"
        return res
    except Exception as e:
        print(e)
        raise security.something_wrong