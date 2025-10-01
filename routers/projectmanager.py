from fastapi import APIRouter, HTTPException, status
from ..utils.dbConn import getConn
from ..utils import security
from datetime import datetime as dt

db = 'projectmanager'

router = APIRouter(
    prefix='/projectmanager'
)

#ProjectManager Exceptions
not_registered = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found to be registered with Project Manager"
)

not_admin = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found to be administrator for Project Manager"
)

is_admin = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You cannot remove priveleges from a Project Manager administrator"
)

project_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Couldn't find project associated with contributors account"
)

not_owner = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You do not own that"
)

is_owner = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You cannot remove an owner"
)

userRoles = [
    ('get', 'projectmanager/project/get'), #Get project data in account from projectID
    ('put', 'projectmanager/project/create'), #Create new project entry
    ('get', 'projectmanager/project/getAll'), #Get all project titles for user
    ('put', 'projectmanager/project/update'), #Update project info TODO
    ('delete', 'projectmanager/project/delete'), #Delete project permenantly (by owner only)
    ('put', 'projectmanager/project/contributors/add'), #Add contributor to a project (shows up in shared projects) (cont. must be registered)
    ('post', 'projectmanager/project/contributors/promote'), #Transfer of ownership (to registered contributor)
    ('post', 'projectmanager/project/contributors/demote'), #Removes ownership from an owner by another owner
    ('post', 'projectmanager/project/contributors/remove'), #Only remove users that aren't project owners. Owners delete project
    ('get', 'projectmanager/project/contributors/getOwners'), #Gets the owners of a project
    ('put', 'projectmanager/project/tag/add'), #Adds the tag to the project
    ('delete', 'projectmanager/project/tag/delete'), #Deletes the tag from the project
    ('put', 'projectmanager/timeEntry/add'), #Add a time entry on a project for a contributor
    ('post', 'projectmanager/timeEntry/edit'), #Edit a time entry TODO
    ('get', 'projectmanager/timeEntry/getByProject'), #Get all time entries by project
    ('get', 'projectmanager/timeEntry/getByContributor'), #Get all time entries by contributor
    ('get', 'projectmanager/timeEntry/get'), #Get by timeEntryID TODO
    ('delete', 'projectmanager/timeEntry/delete'), #Delete a time entry (by id only and will rarely be used if ever)
    ('put', 'projectmanager/tag/create'), #Creates a new tag
    ('get', 'projectmanager/tag/get'), #Gets a tag by name and contributor (Only get your tags)
    ('post', 'projectmanager/tag/update'), #Edits a tag TODO
    ('delete', 'projectmanager/tag/delete') #Deletes a tag (unless projects use it)
]

adminRoles = [
    ('put', 'projectmanager/initialize'), #Initializes database with tables
    ('put', 'projectmanager/user/register'), #Registers a system user with Project Manager roles
    ('put', 'projectmanager/user/promote'), #Promotes Project Manager user to administrator
    ('delete', 'projectmanager/user/demote'), #Demotes Project Manager administrator to registered user
    ('delete', 'projectmanager/user/unregister') #Removes Project Manager roles from system user
]

"""Creates Project Manager database"""
@router.put('/initialize')
async def initialize(token:str):
    data = security.validateToken(token)

    if not security.validateRole(data['sub'], 'put', 'projectmanager/initialize'):
        raise security.unauthorized

    with open('scripts/projectmanager/createStructure.sql') as f:
        query = f.read()
        f.close()

    with open('scripts/getTables.sql') as f:
        query2 = f.read()
        f.close()

    conn = getConn(db)

    with conn.cursor() as cur:
        cur.execute(query)
        cur.close()

    conn.commit()

    with conn.cursor() as cur:
        cur.execute(query2)
        res = cur.fetchall()
        cur.close()

    conn.close()

    return res

"""Binds permissions to system user account for project manager"""
@router.put('/user/register') #TODO: Add registered user to contributors REDO THE RULES FOR WHAT A CONTRIBUTOR IS IN APPDATA INSTEAD
async def registerUser(token:str, username:str):
    data = security.validateToken(token)

    if not security.validateRole(data['sub'], 'put', 'projectmanager/user/register'):
        raise security.unauthorized
    
    with open('scripts/system/role/bind.sql') as f:
        query = f.read()

    conn = getConn('system')

    for role in userRoles:
        params = {
            "username": username,
            "operation": role[0],
            "route": role[1]
        }

        with conn.cursor() as cur:
            cur.execute(query, params)
            cur.close()
        
    conn.commit()

    with open('scripts/system/role/getByUsername.sql') as f:
        query = f.read()
        f.close()

    params = {
        "username": username
    }
    
    with conn.cursor() as cur:
        cur.execute(query, params)
        res = cur.fetchall()
        cur.close()

    conn.close()

    for role in userRoles:
        if role not in res:
            return HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"{role} not in {username} roles: {res}"
            )
        
    return res

"""Adds administrative priveleges for project manager roles"""
@router.put('/user/promote')
async def promoteUser(token:str, username:str):
    data = security.validateToken(token)

    if not security.validateRole(data['sub'], 'put', 'projectmanager/user/promote'):
        raise security.unauthorized
    
    #Check if user is registered as project manager user
    if not security.validateRole(username, 'get', 'projectmanager/project/get'):
        raise not_registered
    
    with open('scripts/system/role/bind.sql') as f:
        query = f.read()
        f.close()

    conn = getConn('system')

    for role in adminRoles:
        params = {
            "username": username,
            "operation": role[0],
            "route": role[1]
        }

        with conn.cursor() as cur:
            cur.execute(query, params)
            cur.close()

    conn.commit()
    
    with open('scripts/system/role/getByUsername.sql') as f:
        query = f.read()
        f.close()

    params = {
        "username": username
    }
    
    with conn.cursor() as cur:
        cur.execute(query, params)
        res = cur.fetchall()
        cur.close()

    conn.close()

    for role in adminRoles:
        if role not in res:
            return HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"{role} not in {username} roles: {res}"
            )
        
    return res

"""Demotes a user to normal project manager user"""
@router.delete('/user/demote')
async def demoteUser(token:str, username:str):
    data = security.validateToken(token)

    if not security.validateRole(data['sub'], 'delete', 'projectmanager/user/demote'):
        raise security.unauthorized
    
    if username == 'admin':
        raise security.admin_infringement
    
    if not security.validateRole(username, 'put', 'projectmanager/user/register'):
        raise not_admin
    
    with open('scripts/system/role/unbind.sql') as f:
        query = f.read()
        f.close()

    conn = getConn('system')

    for role in adminRoles:
        params = {
            "username": username,
            "operation": role[0],
            "route": role[1]
        }

        with conn.cursor() as cur:
            cur.execute(query, params)
            res = cur.fetchall()
            cur.close()
    
    conn.commit()

    if security.validateRole(username, 'put', 'projectmanager/user/register'):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to demote {username}"
        )
    
    return res

"""Deletes user permissions to use project manager"""
@router.delete('/user/unregister')
async def unregisterUser(token:str, username:str): #TODO: Gracefully handle deletion of solo projects and transfer of ownership to other contributors on multi-projects. Also maybe let users delete their own accounts
    data = security.validateToken(token)

    if not security.validateRole(data['sub'], 'delete', 'projectmanager/user/unregister'):
        raise security.unauthorized
    
    if not security.validateRole(username, 'get', 'projectmanager/project/get'):
        raise not_registered
    
    if security.validateRole(username, 'put', 'projectmanager/user/register'):
        raise is_admin
    
    with open('scripts/system/role/unbind.sql') as f:
        query = f.read()
        f.close()

    conn = getConn('system')

    for role in userRoles:
        params = {
            "username": username,
            "operation": role[0],
            "route": role[1]
        }

        with conn.cursor() as cur:
            cur.execute(query, params)
            res = cur.fetchall()
            cur.close()
    
    conn.commit()
    conn.close()

    return res

"""Get a project in users account given project ID"""
@router.get('/project/get')
async def getProject(token:str, ProjectID:int):
    data = security.validateToken(token)

    if not security.validateRole(data['sub'], 'get', 'projectmanager/project/get'):
        raise security.unauthorized
    
    with open('scripts/projectmanager/project/get.sql') as f:
        query = f.read()
        f.close()
    
    conn = getConn(db)

    params = {
        "ProjectID": ProjectID
    }

    with conn.cursor() as cur:
        cur.execute(query, params)
        res = cur.fetchone()
        cur.close()

    conn.close()

    #Check if user is in list of contributors
    if data['appdata']['projectmanager']['contributorID'] not in res[7]:
        raise project_not_found

    return res


"""Create new project in account as owner"""
@router.put('/project/create')
async def createProject(token:str, title:str, devstage:str, description:str, version:str):
    data = security.validateToken(token)

    if not security.validateRole(data['sub'], 'put', 'projectmanager/project/create'):
        raise security.unauthorized
    
    createdAt = dt.now()

    params = {
        "Title": title,
        "DevStage": devstage,
        "Description": description,
        "version": version,
        "StartTime": createdAt,
        "EndTime": createdAt,
        "ContributorID": data['appdata']['projectmanager']['contributorID']
    }

    try:
        with open('scripts/projectmanager/project/create.sql') as f:
            query = f.read()
            f.close()

        conn = getConn(db)

        with conn.cursor() as cur:
            cur.execute(query, params)
            res = cur.fetchone()
            cur.close()

        conn.commit()
        conn.close()

        return res
    except:
        raise security.something_wrong
    
"""Gets all projects the user is a contributor for"""
@router.get('/project/getAll')
async def getAllProjects(token:str,):
    data = security.validateToken(token)

    if not security.validateRole(data['sub'], 'get', 'projectmanager/project/getAll'):
        raise security.unauthorized
    
    params = {
        "ContributorID": data['appdata']['projectmanager']['contributorID']
    }

    try:
        with open('scripts/projectmanager/project/getAll.sql') as f:
            query = f.read()
            f.close()

        conn = getConn(db)

        with conn.cursor() as cur:
            cur.execute(query, params)
            res = cur.fetchall()
            cur.close()
        
        conn.close()

        return res
    except:
        raise security.something_wrong
    

"""Delete project permenantly by owner"""
@router.delete('/project/delete')
async def deleteProject(token:str, projectID:str):
    data = security.validateToken(token)

    if not security.validateRole(data['sub'], 'delete', 'projectmanager/project/delete'):
        raise security.unauthorized
    
    with open('scripts/projectmanager/project/contributors/getOwners.sql') as f:
        query = f.read()
        f.close()

    params = {
        "ProjectID": projectID
    }

    try:

        conn = getConn(db)

        with conn.cursor() as cur:
            cur.execute(query, params)
            res = cur.fetchall()
            cur.close()

        #Check if caller is project owner
        if res[0] != data['appdata']['projectmanager']['contributorID']:
            raise not_owner
        
        with open('scripts/projectmanager/proejct/delete.sql') as f:
            query = f.read()

        with conn.cursor() as cur:
            cur.execute(query, params)
            cur.close()

        conn.commit()
        conn.close()
        return {"detail": "Operation successful"}
    except:
        raise security.something_wrong
    

"""Add contributor to a project (shows up in shared projects) (cont. must be registered)"""
@router.put('/project/contributors/add')
async def addContributorToProject(token:str, projectID:str, contributorID:str, isOwner:bool):
    data = security.validateToken(token)

    if not security.validateRole(data['sub'], 'put', 'projectmanager/project/contributors/add'):
        raise security.unauthorized
    
    params = {
        "ProjectID": projectID,
        "ContributorID": contributorID,
        "IsOwner": isOwner
    }

    with open('scripts/projectmanager/project/contributors/add.sql') as f:
        query = f.read()
        f.close()

    try:
        conn = getConn(db)

        with conn.cursor() as cur:
            cur.execute(query, params)
            res = cur.fetchone()
            cur.close()

        conn.commit()
        conn.close()
        return res
    except:
        raise security.something_wrong
    

"""Promotion to ownership (of registered contributor)"""
@router.post('/project/contributors/promote')
async def promoteContributor(token:str, projectID:str, contributorID:str):
    data = security.validateToken(token)

    if not security.validateRole(data['sub'], 'post', 'projectmanager/project/contributors/promote'):
        raise security.unauthorized
    
    with open('scripts/projectmanager/project/get.sql') as f:
        query = f.read()
        f.close()

    with open('scripts/projectmanager/project/contributors/promote.sql') as f:
        query2 = f.read()
        f.close()

    params = {
        "ProjectID": projectID,
        "ContributorID": contributorID
    }

    try:
        conn = getConn(db)

        with conn.cursor() as cur:
            cur.execute(query, params)
            res = cur.fetchone()
            cur.close()

        if contributorID not in res[7]:
            raise project_not_found

        with conn.cursor() as cur:
            cur.execute(query2, params)
            cur.close()

        conn.commit()
        conn.close()

        return {"detail": "Operation Successful"}
    except:
        raise security.something_wrong
    

"""Removes ownership from project by another owner"""
@router.post('/project/contributors/demote')
async def demoteContributor(token:str, projectID:str, contributorID:str):
    data = security.validateToken(token)

    if not security.validateRole(data['sub'], 'post', 'projectmanager/project/contributors/demote'):
        raise security.unauthorized
    
    with open('scripts/projectmanager/project/get.sql') as f:
        query = f.read()
        f.close()

    with open('scripts/projectmanager/project/contributors/demote.sql') as f:
        query2 = f.read()
        f.close()

    params = {
        "ProjectID": projectID,
        "ContributorID": contributorID
    }

    try:
        conn = getConn(db)

        with conn.cursor() as cur:
            cur.execute(query, params)
            res = cur.fetchone()
            cur.close()

        if contributorID not in res[7]:
            raise project_not_found

        with conn.cursor() as cur:
            cur.execute(query2, params)
            cur.close()

        conn.commit()
        conn.close()

        return {"detail": "Operation Successful"}
    except:
        raise security.something_wrong
    
"""Remove users that aren't project owners from project"""
@router.post('project/contributors/remove')
async def removeContributor(token:str, projectID:str, contributorID:str):
    data = security.validateToken(token)

    if not security.validateRole(data['sub'], 'post', 'projectmanager/project/contributors/remove'):
        raise security.unauthorized
    
    params = {
        "ProjectID": projectID,
        "ContributorID": contributorID
    }

    with open('scripts/projectmanager/proejct/contributors/getOwners.sql') as f:
        query = f.read()
        f.close()

    with open('scripts/projectmanager/project/contributors/remove.sql') as f:
        query2 = f.read()
        f.close()

    try:
        conn = getConn(db)

        with conn.cursor() as cur:
            cur.execute(query, params)
            res = cur.fetchall()
            cur.close()

        if contributorID in res:
            raise is_owner
        
        with conn.cursor() as cur:
            cur.execute(query2, params)
            cur.close()

        conn.commit()
        conn.close()
        return {"detail": "Operation Successful"}
    except:
        raise security.something_wrong
    

"""Get the owners of a project"""
@router.get('/project/contributors/getOwners')
async def getOwners(token:str, projectID:str):
    data = security.validateToken(token)

    if not security.validateRole(data['sub'], 'get', 'projectmanager/project/contributors/getOwners'):
        raise security.unauthorized
    
    with open('scripts/projectmanager/project/contributors/getOwners.sql') as f:
        query = f.read()
        f.close()

    params = {
        "ProjectID": projectID
    }

    try:
        conn = getConn(db)
        with conn.cursor() as cur:
            cur.execute(query, params)
            res = cur.fetchall()
            cur.close()
        conn.close()
        return res
    except:
        raise security.something_wrong
    
"""Adds the tag to the project"""
@router.put('/project/tag/add')
async def bindProjectTag(token:str, projectID:str, tagID:str, isPublic:bool):
    data = security.validateToken(token)

    if not security.validateRole(data['sub'], 'put', 'projectmanager/project/tag/add'):
        raise security.unauthorized
    
    params = {
        "ProjectID": projectID,
        "TagID": tagID,
        "IsPublic": isPublic
    }

    with open('scripts/projectmanager/project/get.sql') as f:
        query = f.read()
        f.close()

    with open('scripts/projectmanager/project/tag/add.sql') as f:
        query2 = f.read()
        f.close()

    try:
        conn = getConn(db)
        with conn.cursor() as cur:
            cur.execute(query, params)
            res = cur.fetchone()
            cur.close()

        if data['appdata']['projectmanager']['contributorID'] not in res[7]:
            raise project_not_found
        
        with conn.cursor() as cur:
            cur.execute(query2, params)
            cur.close()

        conn.commit()
        conn.close()
        return {"detail": "Operation Successful"}
    except:
        raise security.something_wrong
    
"""Deletes a tag from the project"""
@router.delete('/project/tag/delete')
async def unbindProjectTag(token:str, projectID:str, tagID:str):
    data = security.validateToken(token)

    if not security.validateRole(data['sub'], 'delete', 'projectmanager/project/tag/delete'):
        raise security.unauthorized
    
    with open('scripts/projectmanager/project/get.sql') as f:
        query = f.read()
        f.close()

    with open('scripts/projectmanager/project/tag/delete.sql') as f:
        query2 = f.read()
        f.close()

    try:
        conn = getConn(db)
        
        params = {
            "ProjectID": projectID,
            "TagID":  tagID
        }

        with conn.cursor() as cur:
            cur.execute(query, params)
            res = cur.fetchone()
            cur.close()

        if data['appdata']['projectmanager']['contributorID'] not in res[7]:
            raise project_not_found
        
        with conn.cursor() as cur:
            cur.execute(query2, params)
            cur.close()
        
        conn.commit()
        conn.close()
        return {"detail": "Operation Successful"}
    except:
        raise security.something_wrong
    
"""Add a timeEntry on a project for a contributor"""
@router.put('/timeEntry/add')
async def addTimeEntry(token:str, startTime:str, endTime:str, projectID:str, description:str):
    data = security.validateToken(token)

    if not security.validateRole(data['sub'], 'put', 'projectmanager/timeEntry/add'):
        raise security.unauthorized
    
    params = {
        "ProjectID": projectID
    }

    with open('scripts/projectmanager/project/get.sql') as f:
        query = f.read()
        f.close()

    with open('scripts/projectmanager/timeEntry/add.sql') as f:
        query2 = f.read()
        f.close()

    try:
        conn = getConn(db)

        with conn.cursor() as cur:
            cur.execute(query, params)
            res = cur.fetchone()
            cur.close()

        if data['appdata']['projectmanager']['contributorID'] not in res[7]:
            raise project_not_found

        params = {
            "StartTime": startTime,
            "EndTime": endTime,
            "ProjectID": projectID,
            "ContributorID": data['appdata']['projectmanager']['contributorID'],
            "Description": description,
            "Version": res[3]
        }

        with conn.cursor() as cur:
            cur.execute(query2, params)
            res = cur.fetchone()
            cur.close()

        conn.commit()
        conn.close()
        return res
    except:
        raise security.something_wrong

"""Get all time entries by project"""
@router.get('/timeEntry/getByProject')
async def getTimeEntriesByProject(token:str, projectID:str):
    data = security.validateToken(token)

    if not security.validateRole(data['sub'], 'get', 'projectmanager/timeEntry/getByProject'):
        raise security.unauthorized
    
    with open('scripts/projectmanager/project/get.sql') as f:
        query = f.read()
        f.close()
    
    with open('scripts/projectmanager/timeEntry/getByProject.sql') as f:
        query2 = f.read()
        f.close()

    params = {
        "ProjectID": projectID
    }

    try:
        conn = getConn(db)

        with conn.cursor() as cur:
            cur.execute(query, params)
            res = cur.fetchone()
            cur.close()
        
        if data['appdata']['projectmanager']['contributorID'] not in res[7]:
            raise project_not_found
        
        with conn.cursor() as cur:
            cur.execute(query2, params)
            res = cur.fetchall()
            cur.close()

        conn.close()
        return res
    except:
        raise security.something_wrong
    
"""Get all time entries of logged in user"""
@router.get('/timeEntry/getByContributor')
async def getTimeEntriesByContributor(token:str):
    data = security.validateToken(token)

    if not security.validateRole(data['sub'], 'get', 'projectmanager/timeEntry/getByContributor'):
        raise security.unauthorized
    
    params = {
        "ContributorID": data['appdata']['projectmanager']['contributorID']
    }

    with open('scripts/projectmanager/timeEntry/getByContributor.sql') as f:
        query = f.read()
        f.close()

    try:
        conn = getConn(db)

        with conn.cursor() as cur:
            cur.execute(query, params)
            res = cur.fetchall()
            cur.close()

        conn.close()
        return res
    except:
        raise security.something_wrong
    
"""Get time entry by id"""
@router.get('/timeEntry/get')
async def getTimeEntry(token:str, timeEntryID:str):
    data = security.validateToken(token)

    if not security.validateRole(data['sub'], 'get', 'projectmanager/timeEntry/get'):
        raise security.unauthorized
    
    params = {
        "TimeEntryID": timeEntryID
    }

    with open('scripst/projectmanager/timeEntry/get.sql') as f:
        query = f.read()
        f.close()

    try:
        conn = getConn(db)
        
        with conn.cursor() as cur:
            cur.execute(query, params)
            res = cur.fetchone()
            cur.close()

        if res[8] != data['appdata']['projectmanager']['contributorID']:
            raise not_owner
        
        conn.close()
        return res
    except:
        raise security.something_wrong

"""Delete a time entry (by id only and will rarely be used if ever)"""
@router.delete('/timeEntry/delete')
async def deleteTimeEntry(token:str, timeEntryID:str):
    data = security.validateToken(token)

    if not security.validateRole(data['sub'], 'delete', 'projectmanager/timeEntry/delete'):
        raise security.unauthorized
    
    with open('scripts/projectmanager/timeEntry/get.sql') as f:
        query = f.read()
        f.close()

    with open('scripts/projectmanager/timeEntry/delete.sql') as f:
        query2 = f.read()
        f.close()

    params = {
        "TimeEntryID": timeEntryID
    }

    try:
        conn = getConn(db)

        with conn.cursor() as cur:
            cur.execute(query, params)
            res = cur.fetchone()
            cur.close()
        
        if res[8] != data['appdata']['projectmanager']['contributorID']:
            raise project_not_found
        
        with conn.cursor() as cur:
            cur.execute(query2, params)
            cur.close()

        conn.commit()
        conn.close()
        return {"detail": "Operation Successful"}
    except:
        raise security.something_wrong
    
"""Creates a new tag"""
@router.put('/tag/create')
async def createTag(token:str, title:str, implements:str):
    data = security.validateToken(token)

    if not security.validateRole(data['sub'], 'put', 'projectmanager/tag/create'):
        raise security.unauthorized
    
    with open('scripts/projectmanager/tag/create.sql') as f:
        query = f.read()
        f.close()

    params = {
        "Title": title,
        "Implements": implements,
        "OwnerContributorID": data['appdata']['projectmanager']['contributorID']
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
    except:
        raise security.something_wrong
    
"""Deletes a tag (unless projects use it)"""
@router.delete('/tag/delete')
async def deleteTag(token:str, tagID:str):
    data = security.validateToken(token)

    if not security.validateRole(data['sub'], 'delete', 'projectmanager/tag/delete'):
        raise security.unauthorized
    
    params = {
        "TagID": tagID
    }

    with open('scripts/projectmanager/project/tag/getProjects.sql') as f:
        query = f.read()
        f.close()
    
    with open('scripts/projectmanager/tag/delete.sql') as f:
        query2 = f.read()
        f.close()

    try:
        conn = getConn(db)

        with conn.cursor() as cur:
            cur.execute(query, params)
            res = cur.fetchall()
            cur.close()
        
        if res != None:
            return res
        
        with conn.cursor() as cur:
            cur.execute(query2, params)
            cur.close()

        return {"detail": "Operation Successful"}
    except:
        raise security.something_wrong
