"""
Routes: /projectmanager/organization/* => create, dissolve, transfer
"""

from fastapi import APIRouter
from ...utils.dbConn import getConn
from ...utils import security

app = "Project Manager"
db = 'projectmanager'

router = APIRouter(prefix='/organization')

"""Creates an organization owned by the caller"""
@router.put('/create')
async def createOrganization(token:str, orgTitle:str):
    data = security.validateToken(token)
    if not security.validateRole(app, data['role'], 'put', 'projectmanager/organization/create'):
        raise security.unauthorized
    with open('scripts/projectmanager/organization/create.sql') as f:
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
    
"""Dissolves an organization owned by caller, regardless of any other users in it"""
@router.delete('/dissolve')
async def dissolveOrganization(token:str, orgTitle:str):
    data = security.validateToken(token)
    if not security.validateRole(app, data['role'], 'delete', 'projectmanager/organization/dissolve'):
        raise security.unauthorized
    with open('scripts/projectmanager/organization/dissolve.sql') as f:
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
    
"""Transfers ownership of an organization to another contributor"""
@router.post('/transfer')
async def transferOrg(token:str, newOwnerContID:str, orgTitle:str):
    data = security.validateToken(token)
    if not security.validateRole(app, data['role'], 'post', 'projectmanager/organization/transfer'):
        raise security.unauthorized
    with open('scripts/projectmanager/organization/transfer.sql') as f:
        query = f.read()
        f.close()
    params = {
        "ContributorID": data['appdata']['contributorID'],
        "OrgTitle": orgTitle,
        "NewOwnerContID": newOwnerContID
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