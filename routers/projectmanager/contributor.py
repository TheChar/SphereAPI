"""
Routes: /projectmanager/contributor/* => register, leave, organization/join, organization/leave, organization/list
"""
from fastapi import APIRouter
from ...utils.dbConn import getConn
from ...utils import security
from datetime import datetime as dt

db = 'projectmanager'
app = "Project Manager"

router = APIRouter(prefix='/contributor')

"""Registers an existing sphere user to project manager"""
@router.put('/register')
async def registerUser(token:str):
    data = security.validateToken(token)
    if not security.validateRole(app, data['role'], 'put', 'projectmanager/contributor/register'):
        raise security.unauthorized
    with open('scripts/projectmanager/contributor/add.sql') as f:
        query1 = f.read()
        f.close()
    with open('scripts/system/user/register/app.sql') as f:
        query2 = f.read()
        f.close()
    with open('scripts/system/user/getby/username.sql') as f:
        query3 = f.read()
        f.close()
    params = {
        "Username": data['sub'],
        "Name": "Error",
        "AppTitle": app,
        "RoleTitle": "Default",
        "JoinDate": dt.now(),
        "Data": {"contributorID": "-1"}
    }
    try:
        sysconn = getConn('system')
        pmconn = getConn(db)
        with sysconn.cursor() as cur:
            cur.execute(query3, params)
            res = cur.fetchone()
            cur.close()
        name = res[3]
        params["Name"] = name
        with pmconn.cursor() as cur:
            cur.execute(query1, params)
            contID = cur.fetchone()
            cur.close()
        params["Data"]["contributorID"] = contID
        with sysconn.cursor() as cur:
            cur.execute(query2, params)
            cur.close()
        sysconn.commit()
        pmconn.commit()
        sysconn.close()
        pmconn.close()
        return "Success"
    except Exception as e:
        print(e)
        raise security.something_wrong
    
"""Removes a contributor provided all owned projects and organizations have been removed"""
@router.delete('/leave')
async def deactivatePMAccount(token:str):
    data = security.validateToken(token)
    if not security.validateRole(app, data['role'], 'delete', 'projectmanager/contributor/leave'):
        raise security.unauthorized
    with open('scripts/projectmanager/contributor/leave.sql') as f:
        query1 = f.read()
        f.close()
    with open('scripts/system/user/register/leaveApp.sql') as f:
        query2 = f.read()
        f.close()
    params = {
        "contributorID": data['appdata']['contributorID'],
        "AppTitle": app,
        "Username": data['sub'],
    }
    try:
        sysconn = getConn('system')
        pmconn = getConn(db)
        with sysconn.cursor() as cur:
            cur.execute(query2, params)
            cur.close()
        sysconn.commit()
        sysconn.close()
        with pmconn.cursor() as cur:
            cur.execute(query1, params)
            cur.close()
        pmconn.commit()
        pmconn.close()
        return "Success"
    except Exception as e:
        print(e)
        raise security.something_wrong

"""Joins a user to an organization"""
@router.put('/organization/join')
async def joinOrg(token:str, orgTitle:str):
    data = security.validateToken(token)
    if not security.validateRole(app, data['role'], 'put', 'projectmanager/contributor/organization/join'):
        raise security.unauthorized
    with open('scripts/projectmanager/contributor/organization/join.sql') as f:
        query = f.read()
        f.close()
    params = {
        "ContributorID": data['appdata']['contributorID'],
        "OrgTitle": orgTitle
    }
    try:
        conn = getConn(db)
        with conn.cursor() as cur:
            cur.execute(query, params)
            cur.close()
        conn.commit()
        conn.close()
        return "Success"
    except Exception as e:
        print(e)
        raise security.something_wrong
    
"""Removes a contributor from an organization"""
@router.delete('/organization/leave')
async def leaveOrganization(token:str, orgTitle:str):
    data = security.validateToken(token)
    if not security.validateRole(app, data['role'], 'delete', 'projectmanager/contributor/organization/leave'):
        raise security.unauthorized
    with open('scripts/projectmanager/contributor/organization/leave.sql') as f:
        query = f.read()
        f.close()
    params = {
        "ContributorID": data['appdata']['contributorID'],
        "OrgTitle": orgTitle
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
    
"""Gets all organizations associated with contributor"""
@router.get('/organization/list')
async def listOrganizations(token:str):
    data = security.validateToken(token)
    if not security.validateRole(app, data['role'], 'get', 'projectmanager/contributor/organization/list'):
        raise security.unauthorized
    with open('scripts/projectmanager/contributor/organization/list.sql') as f:
        query = f.read()
        f.close()
    params = {
        "ContributorID": data['appdata']['contributorID'],
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