"""
Routes: projectmanager/tag/* => create, update, list/byowner, list/byproject, list/all, get
"""

from fastapi import APIRouter
from ...utils.dbConn import getConn
from ...utils import security
from psycopg2.extras import DictCursor

app = "Project Manager"
db = 'projectmanager'
router = APIRouter(prefix='/tag')

"""Creates a tag"""
@router.put('/create')
async def createTag(token:str, title:str, implements:str, isPublic:str):
    data = security.validateToken(token)
    if not security.validateRole(app, data['role'], 'put', 'projectmanager/tag/create'):
        raise security.unauthorized
    with open('scripts/projectmanager/tag/create.sql') as f:
        query = f.read()
        f.close()
    params = {
        "ContributorID": data['appdata']['contributorID'],
        "Title": title,
        "Implements": implements,
        "IsPublic": isPublic
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
    
"""Updates a tag"""
@router.post('/update')
async def updateTag(token:str, tagID:str, title:str, implements:str, isPublic:str):
    data = security.validateToken(token)
    if not security.validateRole(app, data['role'], 'post', 'projectmanager/tag/update'):
        raise security.unauthorized
    with open('scripts/projectmanager/tag/update.sql') as f:
        query = f.read()
        f.close()
    params = {
        "ContributorID": data['appdata']['contributorID'],
        "Title": title,
        "Implements": implements,
        "TagID": tagID,
        "IsPublic": isPublic
    }
    try:
        conn = getConn(db)
        with conn.cursor() as cur:
            cur.execute("SELECT is_tag_owner(%(ContributorID)s, %(TagID)s)", params)
            res = cur.fetchone()
            if not res[0]:
                raise Exception("User cannot edit properties of a tag they do not own")
            cur.execute(query, params)
            cur.close()
        conn.commit()
        conn.close()
        return "Success"
    except Exception as e:
        print(e)
        raise security.something_wrong
    
"""Lists tags by owner"""
@router.get('/list/byowner')
async def listByOwner(token:str, ownerID:str):
    data = security.validateToken(token)
    if not security.validateRole(app, data['role'], 'get', 'projectmanager/tag/list/byowner'):
        raise security.unauthorized
    with open('scripts/projectmanager/tag/list/byowner.sql') as f:
        query = f.read()
        f.close()
    params = {
        "ContributorID": data['appdata']['contributorID'],
        "OwnerID": ownerID
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
    
"""List tags used in a project provided caller is contributor"""
@router.get('/list/byproject')
async def listByProject(token:str, projectID:str):
    data = security.validateToken(token)
    if not security.validateRole(app, data['role'], 'get', 'projectmanager/tag/list/byproject'):
        raise security.unauthorized
    with open('scripts/projectmanager/tag/list/byproject.sql') as f:
        query = f.read()
        f.close()
    params = {
        "ContributorID": data['appdata']['contributorID'],
        "ProjectID": projectID
    }
    try:
        conn = getConn(db)
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT is_contributor(%(ContributorID)s, %(ProjectID)s)", params)
            res = cur.fetchone()
            if not res['is_contributor']:
                raise Exception("Cannot retrieve information for a project user does not contribute to")
            cur.execute(query, params)
            res = cur.fetchall()
            res = [dict(r) for r in res]
            cur.close()
        conn.close()
        return res
    except Exception as e:
        print(e)
        raise security.something_wrong
    
"""Lists all public tags created by all users"""
@router.get('/list/all')
async def getAllPublicTags(token:str, page:str):
    data = security.validateToken(token)
    if not security.validateRole(app, data['role'], 'get', 'projectmanager/tag/list/all'):
        raise security.unauthorized
    with open('scripts/projectmanager/tag/list/all.sql') as f:
        query = f.read()
        f.close()
    params = {
        "ContributorID": data['appdata']['contributorID'],
        "Page": page
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
    
"""Gets information about a particular tag (checking for public scope against caller)"""
@router.get('/get')
async def getTag(token:str, tagID:str):
    data = security.validateToken(token)
    if not security.validateRole(app, data['role'], 'get', 'projectmanager/tag/get'):
        raise security.unauthorized
    with open('scripts/projectmanager/tag/get.sql') as f:
        query = f.read()
        f.close()
    params = {
        "ContributorID": data['appdata']['contributorID'],
        "TagID": tagID
    }
    try:
        conn = getConn(db)
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT is_tag_owner(%(ContributorID)s, %(TagID)s)", params)
            res = cur.fetchone()
            cur.execute("SELECT is_tag_public(%(TagID)s)", params)
            res2 = cur.fetchone()
            if not res['is_tag_owner'] and not res2['is_tag_public']:
                raise Exception("User cannot access tag data for a private tag they do not own")
            cur.execute(query, params)
            res = cur.fetchall()
            res = [dict(r) for r in res]
            cur.close()
        conn.close()
        return res
    except Exception as e:
        print(e)
        raise security.something_wrong
    
"""Deletes a tag"""
@router.delete('/delete')
async def deleteTag(token:str, tagID:str):
    data = security.validateToken(token)
    if not security.validateRole(app, data['role'], 'delete', 'projectmanager/tag/delete'):
        raise security.unauthorized
    with open('scripts/projectmanager/tag/delete.sql') as f:
        query = f.read()
        f.close()
    params = {
        "ContributorID": data['appdata']['contributorID'],
        "TagID": tagID
    }
    try:
        conn = getConn(db)
        with conn.cursor() as cur:
            cur.execute("SELECT is_tag_owner(%(ContributorID)s, %(TagID)s)", params)
            res = cur.fetchone()
            if not res[0]:
                raise Exception("User cannot delete a tag they do not own")
            cur.execute(query, params)
            cur.close()
        conn.commit()
        conn.close()
        return "Success"
    except Exception as e:
        print(e)
        raise security.something_wrong