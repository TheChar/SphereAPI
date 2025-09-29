from fastapi import APIRouter, HTTPException, status
from ..utils.dbConn import getConn
from ..utils import security

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

userRoles = [
    ('get', 'projectmanager/project/get'), #Get project data
    ('put', 'projectmanager/project/create'), #Create new project entry
    ('get', 'projectmanager/project/getAll'), #Get all project titles for user
    ('put', 'projectmanager/project/update'), #Update project info
    ('delete', 'projectmanager/project/delete'), #Delete project permenantly (by owner only)
    ('put', 'projectmanager/project/contributors/add'), #Add contributor to a project (shows up in shared projects) (cont. must be registered)
    ('post', 'projectmanager/project/contributors/promote'), #Transfer of ownership (to registered contributor)
    ('post', 'projectmanager/project/contributors/remove'), #Only remove users that aren't project owners. Owners delete project
    ('put', 'projectmanager/project/tag/add'), #Adds the tag to the project
    ('delete', 'projectmanager/project/tag/delete'), #Deletes the tag from the project
    ('put', 'projectmanager/timeEntry/add'), #Add a time entry on a project for a contributor
    ('post', 'projectmanager/timeEntry/edit'), #Edit a time entry
    ('get', 'projectmanager/timeEntry/get'), #Get all time entries by project
    ('delete', 'projectmanager/timeEntry/delete'), #Delete a time entry (by id only and will rarely be used if ever)
    ('put', 'projectmanager/tag/create'), #Creates a new tag
    ('get', 'projectmanager/tag/get'), #Gets a tag by name
    ('post', 'projectmanager/tag/update') #Edits a tag
]

adminRoles = [
    ('put', 'projectmanager/initialize'), #Initializes database with tables
    ('put', 'projectmanager/user/register'), #Registers a system user with Project Manager roles
    ('put', 'projectmanager/user/promote'), #Promotes Project Manager user to administrator
    ('delete', 'projectmanager/user/demote'), #Demotes Project Manager administrator to registered user
    ('delete', 'projectmanager/user/unregister'), #Removes Project Manager roles from system user
    ('delete', 'projectmanager/tag/delete') #Deletes a tag (gracefully handling projects that have the tag)
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

    conn = getConn('projectmanager')

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
@router.put('/user/register')
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

@router.get('/project/get')
async def getProject(token:str):
    data = security.validateToken(token)

    if not security.validateRole(data['sub'], 'get', 'projectmanager/project/get'):
        raise security.unauthorized
    
    return "You got a project"