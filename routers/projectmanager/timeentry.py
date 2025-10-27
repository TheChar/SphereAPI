"""
Routes: /projectmanager/timeentry/* => create, update, delete, list/byproject, list/bycontributor
"""

from fastapi import APIRouter
from ...utils.dbConn import getConn
from ...utils import security
from psycopg2.extras import DictCursor

db = 'projectmanager'
app = "Project Manager"
router = APIRouter(prefix='/timeentry')

"""Creates a new time entry"""
@router.put('/create')
async def createTimeEntry(token:str, projectID:str, description:str, version:str):
    data = security.validateToken(token)
    if not security.validateRole(app, data['role'], 'put', 'projectmanager/timeentry/create'):
        raise security.unauthorized
    with open('scripts/projectmanager/timeentry/create.sql') as f:
        query = f.read()
        f.close()
    params = {
        "ContributorID": data['appdata']['contributorID'],
        "ProjectID": projectID,
        "Description": description,
        "Version": version
    }
    try:
        conn = getConn(db)
        with conn.cursor() as cur:
            cur.execute("is_contributor(%(ContributorID)s, %(ProjectID)s)", params)
            res = cur.fetchone()
            if not res[0]:
                raise Exception('User cannot create time entries for projects they do not contribute to')
            cur.execute(query, params)
            cur.close()
        conn.commit()
        conn.close()
        return "Success"
    except Exception as e:
        print(e)
        raise security.something_wrong
    
"""Updates a timeentry"""
@router.post('/update')
async def updateTimeEntry(token:str, timeEntryID:str, startTime:str, endTime:str, description:str, version:str):
    data = security.validateToken(token)
    if not security.validateRole(app, data['role'], 'post', 'projectmanager/timeentry/update'):
        raise security.unauthorized
    with open('scripts/projectmanager/timeentry/update.sql') as f:
        query = f.read()
        f.close()
    params = {
        "ContributorID": data['appdata']['contributorID'],
        "TimeEntryID": timeEntryID,
        "StartTime": startTime,
        "EndTime": endTime,
        "Description": description,
        "Version": version
    }
    try:
        conn = getConn(db)
        with conn.cursor() as cur:
            cur.execute("SELECT is_timeentry_owner(%(ContributorID)s, %(TimeEntryID)s)", params)
            res = cur.fetchone()
            if not res[0]:
                raise Exception("User cannot update an entry that does not belong to them")
            cur.execute(query, params)
            cur.close()
        conn.commit()
        conn.close()
        return "Success"
    except Exception as e:
        print(e)
        raise security.something_wrong
    
"""Deletes a time entry"""
@router.delete('/delete')
async def deleteEntry(token:str, timeEntryID:str):
    data = security.validateToken(token)
    if not security.validateRole(app, data['role'], 'delete', 'projectmanager/timeentry/delete'):
        raise security.unauthorized
    with open('scripts/projectmanager/timeentry/delete.sql') as f:
        query = f.read()
        f.close()
    params = {
        "ContributorID": data['appdata']['contributorID'],
        "TimeEntryID": timeEntryID
    }
    try:
        conn = getConn(db)
        with conn.cursor() as cur:
            cur.execute("SELECT is_timeentry_owner(%(ContributorID)s, %(TimeEntryID)s)", params)
            res = cur.fetchone()
            if not res[0]:
                raise Exception("User cannot delete time entry that does not belong to them")
            cur.execute(query, params)
            cur.close()
        conn.commit()
        conn.close()
        return "Success"
    except Exception as e:
        print(e)
        raise security.something_wrong
    
"""List time entries by project"""
@router.get('/list/byproject')
async def listByProject(token:str, projectID:str):
    data = security.validateToken(token)
    if not security.validateRole(app, data['role'], 'get', 'projectmanager/timeentry/list/byproject'):
        raise security.unauthorized
    with open('scripts/projectmanager/timeentry/list/byproject.sql') as f:
        query = f.read()
        f.close()
    params = {
        "ContributorID": data['appdata']['contributorID'],
        "ProjectID": projectID
    }
    try:
        conn = getConn(db)
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("is_contributor(%(ContributorID)s, %(ProjectID)s)", params)
            res = cur.fetchone()
            if not res['is_contributor']:
                raise Exception("User cannot get time entries for a project they do not contribute to")
            cur.execute(query, params)
            res = cur.fetchall()
            res = [dict(r) for r in res]
            cur.close()
        conn.close()
        return res
    except Exception as e:
        print(e)
        raise security.something_wrong
    
"""Lists time entries by contributor (for self only)"""
@router.get('/list/bycontributor')
async def listByContributor(token:str):
    data = security.validateToken(token)
    if not security.validateRole(app, data['role'], 'get', 'projectmanager/timeentry/list/bycontributor'):
        raise security.unauthorized
    with open('scripts/projectmanager/timeentry/list/bycontributor.sql') as f:
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