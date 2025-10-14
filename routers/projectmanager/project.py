"""
Routes: /projectmanager/project/* => create, update, delete, get, transfer, list/all, list/byowner, list/bytag, contributor/add, contributor/remove, contributor/restore, tag/bind, tag/unbind, tag/get
"""

from fastapi import APIRouter
from ...utils.dbConn import getConn
from ...utils import security

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
            res = cur.fetchone()
            cur.close()
        conn.commit()
        conn.close()
        return res
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
    params = {
        "ContributorID": data['appdata']['contributorID'],
        "ProjectID": projectID,
        "Title": title,
        "Description": description,
        "Version": version
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
            res = cur.fetchone()
            cur.close()
        conn.commit()
        conn.close()
        return res
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
        with conn.cursor() as cur:
            cur.execute(query, params)
            res = cur.fetchone()
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
    
"""Gets all projects worked on by caller"""
@router.get('/list/all')
async def listProjects(token:str):
    data = security.validateToken(token)
    if not security.validateRole(app, data['role'], 'get', 'projectmanager/project/list/all'):
        raise security.unauthorized
    with open('scripts/projectmanager/project/list/all.sql') as f:
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
        with conn.cursor() as cur:
            cur.execute(query, params)
            res = cur.fetchall()
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
        with conn.cursor() as cur:
            cur.execute(query, params)
            res = cur.fetchall()
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
            cur.execute(query, params)
            res = cur.fetchone()
            cur.close()
        conn.commit()
        conn.close()
        return res
    except Exception as e:
        print(e)
        raise security.something_wrong
    
"""Removes a contributor from a project with bit flippling"""
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
            cur.execute(query, params)
            res = cur.fetchone()
            cur.close()
        conn.commit()
        conn.close()
        return res
    except Exception as e:
        print(e)
        raise security.something_wrong
    
"""Restores a contributor previously removed from a project by the owner only"""
@router.post('/contributor/restore')
async def restoreContributor(token:str, projectID:str, restoredContID:str):
    data = security.validateToken(token)
    if not security.validateRole(app, data['role'], 'post', 'projectmanager/project/contributor/restore'):
        raise security.unauthorized
    with open('scripts/projectmanager/project/contributor/restore.sql') as f:
        query = f.read()
        f.close()
    params = {
        "ContributorID": data['appdata']['contributorID'],
        "RestoredContributorID": restoredContID,
        "ProjectID": projectID
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

"""Binds a tag to a project user is contributor of"""
@router.put('/tag/bind')
async def bindTag(token:str, projectID:str, tagID:str):
    data = security.validateToken(token)
    if not security.validateRole(app, data['role'], 'put', 'projectmanager/project/tag/bind'):
        raise security.unauthorized
    with open('scripts/projectmanager/project/tag/bind.sql') as f:
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
            cur.execute(query, params)
            res = cur.fetchone()
            cur.close()
        conn.commit()
        conn.close()
        return res
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
            cur.execute(query, params)
            res = cur.fetchone()
            cur.close()
        conn.commit()
        conn.close()
        return res
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
        with conn.cursor() as cur:
            cur.execute(query, params)
            res = cur.fetchone()
            cur.close()
        conn.close()
        return res
    except Exception as e:
        print(e)
        raise security.something_wrong