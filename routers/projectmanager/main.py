from fastapi import APIRouter
from ...utils.dbConn import getConn
from ...utils import security

router = APIRouter(prefix='/projectmanager')
db = 'projectmanager'

@router.get('/')
async def onlineCheck():
    return "Project Manager API is online"

@router.put('/initialize')
async def initialize():
    # raise HTTPException(
    #     status_code=status.HTTP_403_FORBIDDEN,
    #     detail="This route does not exist"
    # )
    conn = getConn(db)
    with open('scripts/projectmanager/initialize.sql') as f:
        query = f.read()
        f.close()

    with conn.cursor() as cur:
        cur.execute(query)
        cur.close()

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

    conn.commit()

    conn.close()

    return {"detail": "Operation Successful"}