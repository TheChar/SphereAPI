"""
Routes: /projectmanager/project/* => create, update, delete, get, transfer, list/all, list/byowner, list/bytag, contributor/add, contributor/remove, contributor/restore, tag/bind, tag/unbind, tag/get
"""

from fastapi import APIRouter
from ...utils.dbConn import getConn
from ...utils import security
from psycopg2.extras import DictCursor

app = "Project Manager"
db = 'projectmanager'
router = APIRouter(prefix='/project')

"""Creates a project"""
@router.put('/create')
async def createProject(token:str, title:str, description:str, version:str):
    data = security.validateToken(token)
    if not security.validateRole(app, data['role'], 'put', 'projectmanager/project/create'):
        raise security.unauthorized
    with open('scripts/projectmanager/project/create.sql') as f:
        query = f.read()
        f.close()
    params = {
        "ContributorID": data['appdata']['contributorID'],
        "Title": title,
        "Description": description,
        "Version": version
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
    
"""Updates a project if caller owns it"""
@router.post('/update')
async def updateProject(token:str, projectID:str, title:str, description:str, version:str):
    data = security.validateToken(token)
    if not security.validateRole(app, data['role'], 'post', 'projectmanager/project/update'):
        raise security.unauthorized
    with open('scripts/projectmanager/project/update.sql') as f:
        query = f.read()
        f.close()
    print('read in a query')
    params = {
        "ContributorID": data['appdata']['contributorID'],
        "ProjectID": projectID,
        "Title": title if title != '' else None,
        "Description": description if description != '' else None,
        "Version": version if version != '' else None
    }
    try:
        conn = getConn(db)
        with conn.cursor() as cur:
            cur.execute("SELECT is_owner(%(ContributorID)s, %(ProjectID)s)", params)
            res = cur.fetchone()
            if not res[0]:
                raise Exception("User cannot edit metadata on a project they do not own")
            cur.execute(query, params)
            cur.close()
        conn.commit()
        conn.close()
        return "Success"
    except Exception as e:
        print(e)
        raise security.something_wrong
    
"""Deletes a project if caller owns it"""
@router.delete('/delete')
async def deleteProject(token:str, projectID:str):
    data = security.validateToken(token)
    if not security.validateRole(app, data['role'], 'delete', 'projectmanager/project/delete'):
        raise security.unauthorized
    with open('scripts/projectmanager/project/delete.sql') as f:
        query = f.read()
        f.close()
    params = {
        "ContributorID": data['appdata']['contributorID'],
        "ProjectID": projectID,
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
    
"""Get all info related to a project given by id provided caller is a contributor"""
@router.get('/get')
async def getProjectInfo(token:str, projectID:str):
    data = security.validateToken(token)
    if not security.validateRole(app, data['role'], 'get', 'projectmanager/project/get'):
        raise security.unauthorized
    with open('scripts/projectmanager/project/get.sql') as f:
        query = f.read()
        f.close()
    params = {
        "ContributorID": data['appdata']['contributorID'],
        "ProjectID": projectID,
    }
    try:
        conn = getConn(db)
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT is_contributor(%(ContributorID)s, %(ProjectID)s)", params)
            res = cur.fetchone()
            if not res[0]:
                raise Exception('User is not a contributor')
            cur.execute(query, params)
            res = cur.fetchall()
            res = [dict(r) for r in res]
            cur.close()
        conn.close()
        return res
    except Exception as e:
        print(e)
        raise security.something_wrong
    
"""Transfer ownership of a project to a different contributor"""
@router.post('/transfer')
async def transferOwnership(token:str, projectID:str, newOwnerID:str):
    data = security.validateToken(token)
    if not security.validateRole(app, data['role'], 'post', 'projectmanager/project/transfer'):
        raise security.unauthorized
    with open('scripts/projectmanager/project/transfer.sql') as f:
        query = f.read()
        f.close()
    params = {
        "ContributorID": data['appdata']['contributorID'],
        "ProjectID": projectID,
        "NewOwnerID": newOwnerID
    }
    try:
        conn = getConn(db)
        with conn.cursor() as cur:
            cur.execute("SELECT is_owner(%(ContributorID)s, %(ProjectID)s)", params)
            res = cur.fetchone()
            if not res[0]:
                raise Exception("User cannot edit transfer a project they do not own")
            cur.execute("SELECT is_contributor(%(NewOwnerID)s, %(ProjectID)s)", params)
            res = cur.fetchone()
            if not res[0]:
                raise Exception("User cannot tranfer a project to someone who is not a contributor")
            cur.execute(query, params)
            cur.close()
        conn.commit()
        conn.close()
        return "Success"
    except Exception as e:
        print(e)
        raise security.something_wrong
    
"""Gets all projects worked on by caller"""
@router.get('/list/all')
async def listAllProjects(token:str):
    data = security.validateToken(token)
    if not security.validateRole(app, data['role'], 'get', 'projectmanager/project/list/all'):
        raise security.unauthorized
    with open('scripts/projectmanager/project/list/all.sql') as f:
        query = f.read()
        f.close()
    params = {
        "ContributorID": data['appdata']['contributorID']
    }
    # try:
    conn = getConn(db)
    with conn.cursor(cursor_factory=DictCursor) as cur:
        cur.execute(query, params)
        res = cur.fetchall()
        res = [dict(r) for r in res]
        cur.close()
    conn.close()
    return res
    # except Exception as e:
    #     print(e)
    #     raise security.something_wrong
    
"""Gets all projects owned by caller"""
@router.get('/list/byowner')
async def listOwnedProjects(token:str):
    data = security.validateToken(token)
    if not security.validateRole(app, data['role'], 'get', 'projectmanager/project/list/byowner'):
        raise security.unauthorized
    with open('scripts/projectmanager/project/list/byowner.sql') as f:
        query = f.read()
        f.close()
    params = {
        "ContributorID": data['appdata']['contributorID']
    }
    try:
        conn = getConn(db)
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(query, params)
            res = cur.fetchall()
            res = [dict(r) for r in res]
            cur.close()
        conn.close()
        return res
    except Exception as e:
        print(e)
        raise security.something_wrong

"""Gets all project implementing a tag owned by caller"""
@router.get('/list/bytag')
async def listByTag(token:str, tagTitle:str):
    data = security.validateToken(token)
    if not security.validateRole(app, data['role'], 'get', 'projectmanager/project/list/bytag'):
        raise security.unauthorized
    with open('scripts/projectmanager/project/list/bytag.sql') as f:
        query = f.read()
        f.close()
    params = {
        "ContributorID": data['appdata']['contributorID'],
        "TagTitle": tagTitle
    }
    try:
        conn = getConn(db)
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(query, params)
            res = cur.fetchall()
            res = [dict(r) for r in res]
            cur.close()
        conn.close()
        return res
    except Exception as e:
        print(e)
        raise security.something_wrong
    
"""Adds a contributor to a project"""
@router.put('/contributor/add')
async def addContributor(token:str, projectID:str, newContributorID:str):
    data = security.validateToken(token)
    if not security.validateRole(app, data['role'], 'put', 'projectmanager/project/contributor/add'):
        raise security.unauthorized
    with open('scripts/projectmanager/project/contributor/add.sql') as f:
        query = f.read()
        f.close()
    params = {
        "ContributorID": data['appdata']['contributorID'],
        "ProjectID": projectID,
        "NewContributorID": newContributorID
    }
    try:
        conn = getConn(db)
        with conn.cursor() as cur:
            cur.execute("SELECT is_contributor(%(ContributorID)s, %(ProjectID)s)", params)
            res = cur.fetchone()
            if not res[0]:
                raise Exception('Cannot add to a project not contributing to')
            cur.execute(query, params)
            cur.close()
        conn.commit()
        conn.close()
        return "Success"
    except Exception as e:
        print(e)
        raise security.something_wrong
    
"""Removes a contributor from a project (field altering, not record dropping)"""
@router.post('/contributor/remove')
async def removeContributor(token:str, projectID:str, removedContributorID:str):
    data = security.validateToken(token)
    if not security.validateRole(app, data['role'], 'post', 'projectmanager/project/contributor/remove'):
        raise security.unauthorized
    with open('scripts/projectmanager/project/contributor/remove.sql') as f:
        query = f.read()
        f.close()
    params = {
        "ContributorID": data['appdata']['contributorID'],
        "ProjectID": projectID,
        "RemovedContributorID": removedContributorID
    }
    try:
        conn = getConn(db)
        with conn.cursor() as cur:
            cur.execute("SELECT is_owner(%(ContributorID)s, %(ProjectID)s)", params)
            res = cur.fetchone()
            if res[0] and str(data['appdata']['contributorID']) == str(removedContributorID):
                raise Exception("Owner cannot remove self. Transfer project or delete.")
            elif not res[0] and (str(data['appdata']['contributorID']) != str(removedContributorID)):
                raise Exception(f"Non-owner cannot remove other contributors from project. Owner state: {res[0]}. Caller: {data['appdata']['contributorID']}. Removed: {removedContributorID}")
            cur.execute(query, params)
            cur.close()
        conn.commit()
        conn.close()
        return "Success"
    except Exception as e:
        print(e)
        raise security.something_wrong
    
"""Restores a contributor previously removed from a project by the owner only"""
@router.post('/contributor/restore')
async def restoreContributor(token:str, projectID:str, restoredContributorID:str):
    data = security.validateToken(token)
    if not security.validateRole(app, data['role'], 'post', 'projectmanager/project/contributor/restore'):
        raise security.unauthorized
    with open('scripts/projectmanager/project/contributor/restore.sql') as f:
        query = f.read()
        f.close()
    params = {
        "ContributorID": data['appdata']['contributorID'],
        "RestoredContributorID": restoredContributorID,
        "ProjectID": projectID
    }
    try:
        conn = getConn(db)
        with conn.cursor() as cur:
            cur.execute("SELECT is_owner(%(ContributorID)s, %(ProjectID)s)", params)
            res = cur.fetchone()
            if not res[0]:
                raise Exception("Only an owner can restore a previously removed contributor")
            cur.execute(query, params)
            cur.close()
        conn.commit()
        conn.close()
        return "Success"
    except Exception as e:
        print(e)
        raise security.something_wrong
    
"""Gets a list of contributor data for a project"""
@router.get('/contributor/list')
async def listProjectContributors(token:str, projectID:str):
    data = security.validateToken(token)
    if not security.validateRole(app, data['role'], 'get', 'projectmanager/project/contributor/list'):
        raise security.unauthorized
    with open('scripts/projectmanager/project/contributor/list.sql') as f:
        query = f.read()
        f.close()
    params = {
        "ContributorID": data['appdata']['contributorID'],
        "ProjectID": projectID
    }
    try:
        conn = getConn(db)
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute('SELECT is_contributor(%(ContributorID)s, %(ProjectID)s)', params)
            res = cur.fetchone()
            if not res[0]:
                raise Exception("Cannot view contributor list for project not contributing to")
            cur.execute(query, params)
            res = cur.fetchall()
            res = [dict(r) for r in res]
            cur.close()
        return res
    except Exception as e:
        print(e)
        raise security.something_wrong


"""Binds a tag to a project user is contributor of"""
@router.put('/tag/bind')
async def bindTag(token:str, projectID:str, tagID:str, implementations:str):
    data = security.validateToken(token)
    if not security.validateRole(app, data['role'], 'put', 'projectmanager/project/tag/bind'):
        raise security.unauthorized
    with open('scripts/projectmanager/project/tag/bind.sql') as f:
        query = f.read()
        f.close()
    params = {
        "ContributorID": data['appdata']['contributorID'],
        "TagID": tagID,
        "ProjectID": projectID,
        "Implementations": implementations
    }
    #TODO: Parse incoming implementations to make sure they are ok
    try:
        conn = getConn(db)
        with conn.cursor() as cur:
            cur.execute("SELECT is_contributor(%(ContributorID)s, %(ProjectID)s)", params)
            res = cur.fetchone()
            if not res[0]:
                raise Exception("Cannot add tag to a project user is not contributor of")
            #TODO: Needs to check if the implementations are the types and formats expected by the tag
            cur.execute(query, params)
            cur.close()
        conn.commit()
        conn.close()
        return "Success"
    except Exception as e:
        print(e)
        raise security.something_wrong
    
"""Unbinds a tag from a project"""
@router.delete('/tag/unbind')
async def unbindTag(token:str, projectID:str, tagID:str):
    data = security.validateToken(token)
    if not security.validateRole(app, data['role'], 'delete', 'projectmanager/project/tag/unbind'):
        raise security.unauthorized
    with open('scripts/projectmanager/project/tag/unbind.sql') as f:
        query = f.read()
        f.close()
    params = {
        "ContributorID": data['appdata']['contributorID'],
        "TagID": tagID,
        "ProjectID": projectID
    }
    try:
        conn = getConn(db)
        with conn.cursor() as cur:
            cur.execute("SELECT is_contributor(%(ContributorID)s, %(ProjectID)s)", params)
            res = cur.fetchone()
            if not res[0]:
                raise Exception('User cannot edit a project they do not contribute to')
            cur.execute(query, params)
            cur.close()
        conn.commit()
        conn.close()
        return "Success"
    except Exception as e:
        print(e)
        raise security.something_wrong
    
"""Gets tag implementation used by a specific project"""
@router.get('/tag/get')
async def getTagImplementation(token:str, projectID:str, tagID:str):
    data = security.validateToken(token)
    if not security.validateRole(app, data['role'], 'get', 'projectmanager/project/tag/get'):
        raise security.unauthorized
    with open('scripts/projectmanager/project/tag/get.sql') as f:
        query = f.read()
        f.close()
    params = {
        "ContributorID": data['appdata']['contributorID'],
        "ProjectID": projectID,
        "TagID": tagID
    }
    try:
        conn = getConn(db)
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT is_contributor(%(ContributorID)s, %(ProjectID)s)", params)
            res = cur.fetchone()
            if not res['is_contributor']:
                raise Exception("Cannot access data for a project not contributing to")
            cur.execute(query, params)
            res = cur.fetchall()
            res = [dict(r) for r in res]
            cur.close()
        conn.close()
        return res
    except Exception as e:
        print(e)
        raise security.something_wrong