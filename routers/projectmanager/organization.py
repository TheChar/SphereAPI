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
async def transferOrg(token:str, newOwnerContID:str, orgID:str):
    data = security.validateToken(token)
    if not security.validateRole(app, data['role'], 'post', 'projectmanager/organization/transfer'):
        raise security.unauthorized
    with open('scripts/projectmanager/organization/transfer.sql') as f:
        query = f.read()
        f.close()
    params = {
        "ContributorID": data['appdata']['contributorID'],
        "OrganizationID": orgID,
        "NewOwnerContID": newOwnerContID
    }
    try:
        conn = getConn(db)
        with conn.cursor() as cur:
            cur.execute("SELECT is_in_organization(%(NewOwnerContID)s, %(OrganizationID)s)", params)
            res = cur.fetchone()
            cur.execute("SELECT is_organization_owner(%(ContributorID)s, %(OrganizationID)s)", params)
            res2 = cur.fetchone()
            if not res[0]:
                raise Exception('Cannot transfer ownership to a non-member')
            if not res2[0]:
                raise Exception('Cannot transfer ownership if not owner')
            cur.execute(query, params)
            cur.close()
        conn.commit()
        conn.close()
        return "Success"
    except Exception as e:
        print(e)
        raise security.something_wrong
    
"""Invites a user to join an organization"""
@router.put('/invite')
async def inviteToOrg(token:str, orgID:str, newContID:str):
    data = security.validateToken(token)
    if not security.validateRole(app, data['role'], 'put', 'projectmanager/organization/invite'):
        raise security.unauthorized
    with open('scripts/projectmanager/organization/invite.sql') as f:
        query = f.read()
        f.close()
    params = {
        "OrganizationID": orgID,
        "NewContributorID": newContID,
        "ContributorID": data['appdata']['contributorID']
    }
    try:
        conn = getConn(db)
        with conn.cursor() as cur:
            cur.execute("SELECT is_in_organization(%(ContributorID)s, %(OrganizationID)s)", params)
            res = cur.fetchone()
            if not res[0]:
                raise Exception('Cannot invite to an organization not already in')
            cur.execute(query, params)
            cur.close()
        conn.commit()
        conn.close()
        return "Success"
    except Exception as e:
        print(e)
        raise security.something_wrong
        