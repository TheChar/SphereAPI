import requests
import pytest
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

baseurl = "http://localhost:8000/system"

def callAPI(method, path):
    url = baseurl + path
    match(method):
        case 'get':
            res = requests.get(url)
        case 'put':
            res = requests.put(url)
        case 'delete':
            res = requests.delete(url)
        case 'post':
            res = requests.post(url)
        case _:
            raise Exception('Invalid Method type')
    return res

def getToken(type):
    if type == 'admin':
        res = callAPI('post', '/token?username=testsoftware&password=password&appTitle=System')
    elif type == 'default':
        res = callAPI('post', '/token?username=testsoftwaredefault&password=password&appTitle=System')
    else: 
        res = callAPI('post', '/token')
    token = res.json()
    return token

"""Creates testing accounts"""
def test_init():
    res = callAPI('post', '/token?username=admin&password=password&appTitle=System')
    token = res.json()
    callAPI('put', f'/user/add?token={token}&username=testsoftware&password=password&name=Admin Test Software')
    callAPI('put', f'/user/register/role?token={token}&appTitle=System&roleTitle=Admin&username=testsoftware')
    callAPI('put', f'/user/add?token={token}&username=testsoftwaredefault&password=password&name=Default Test Software')

"""Tests app listing arriving in correct format"""
def test_listapps():
    token = getToken('admin')
    res = callAPI('get', f'/application/list?token={token}')
    parsed = res.json()
    assert res.ok
    assert isinstance(parsed, list)
    assert ["System"] in parsed

    token = getToken('default')
    res = callAPI('get', f'/application/list?token={token}')
    parsed = res.json()
    assert not res.ok
    assert isinstance(parsed, dict)
    assert 'detail' in parsed.keys()

"""Tests configuration endpoint (runs once then errors)"""
def test_configdb():
    res = callAPI('put', '/sysdb')
    assert not res.ok

"""Tests initializer endpoint (runs once then errors)"""
def test_initializer():
    res = callAPI('put', '/initialize')
    assert not res.ok

"""Tests database lists"""
def test_databaseList():
    token = getToken('admin')
    res = callAPI('get', f'/database/list?token={token}')
    parsed = res.json()
    assert res.ok
    assert isinstance(parsed, list)
    assert ['system'] in parsed

    token = getToken('default')
    res = callAPI('get', f'/database/list?token={token}')
    assert not res.ok
    assert res.status_code == 401

"""Tests database creation"""
def test_databaseCreate():
    token = getToken('admin')
    res = callAPI('put', f'/database/create?token={token}&name=test')
    assert res.ok
    res = callAPI('get', f'/database/list?token={token}')
    parsed = res.json()
    assert res.ok
    assert isinstance(parsed, list)
    assert ['test'] in parsed

    token = getToken('default')
    res = callAPI('put', f'/database/create?token={token}&name=test')
    assert not res.ok
    assert res.status_code == 401

"""Tests database deletion"""
def test_databaseDelete():
    token = getToken('admin')
    res = callAPI('delete', f'/database/delete?token={token}&name=test')
    parsed = res.json()
    assert res.ok
    assert parsed['message'] == 'Operation Complete'

    token = getToken('default')
    res = callAPI('delete', f'/database/delete?token={token}&name=test')
    assert not res.ok
    assert res.status_code == 401

"""List Applications"""
def test_applicationList():
    token = getToken('admin')
    res = callAPI('get', f'/application/list?token={token}')
    parsed = res.json()
    assert res.ok
    assert isinstance(parsed, list)
    assert ['System'] in parsed

    token = getToken('default')
    res = callAPI('get', f'/application/list?token={token}')
    assert not res.ok
    assert res.status_code == 401

"""Get applications"""
def test_applicationGet():
    token = getToken('admin')
    res = callAPI('get', f'/application/get?token={token}&title=System')
    parsed = res.json()
    assert res.ok
    assert isinstance(parsed, list)
    assert isinstance(parsed[0], int)
    assert parsed[1] == "System"
    assert isinstance(parsed[2], list)

    token = getToken('default')
    res = callAPI('get', f'/application/get?token={token}&title=System')
    assert not res.ok
    assert res.status_code == 401

"""Add applications"""
def test_applicationAdd():
    token = getToken('admin')
    res = callAPI('put', f'/application/add?token={token}&title=Test')
    callAPI('put', f'/role/add?token={token}&roleTitle=Default&appTitle=Test&description=Default role')
    parsed = res.json()
    assert res.ok
    assert isinstance(parsed, list)
    assert isinstance(parsed[0], int)

    token = getToken('default')
    res = callAPI('put', f'/application/add?token={token}&title=Test')
    assert not res.ok
    assert res.status_code == 401

"""List roles"""
def test_roleList():
    token = getToken('admin')
    res = callAPI('get', f'/role/list?token={token}&appTitle=System')
    parsed = res.json()
    assert res.ok
    assert isinstance(parsed, list)
    assert ['Default'] in parsed
    assert ['Admin'] in parsed
    
    token = getToken('default')
    res = callAPI('get', f'/role/list?token={token}&appTitle=System')
    assert not res.ok
    assert res.status_code == 401

"""Get roles from system"""
def test_roleGet():
    token = getToken('admin')
    res = callAPI('get', f'/role/get?token={token}&appTitle=System&roleTitle=Default')
    parsed = res.json()
    assert res.ok
    assert isinstance(parsed, list)
    print(parsed)
    assert isinstance(parsed[0], int)
    assert parsed[1] == 'Default'
    assert isinstance(parsed[2], str)
    assert isinstance(parsed[3], int)

    token = getToken('admin')
    res = callAPI('get', f'/role/get?token={token}&appTitle=System&roleTitle=Admin')
    parsed = res.json()
    assert res.ok
    assert isinstance(parsed, list)
    print(parsed)
    assert isinstance(parsed[0], int)
    assert parsed[1] == 'Admin'
    assert isinstance(parsed[2], str)
    assert isinstance(parsed[3], int)

    token = getToken('default')
    res = callAPI('get', f'/role/get?token={token}&appTitle=System&roleTitle=Default')
    assert not res.ok
    assert res.status_code == 401

    token = getToken('default')
    res = callAPI('get', f'/role/get?token={token}&appTitle=System&roleTitle=Admin')
    assert not res.ok
    assert res.status_code == 401

"""Add a role"""
def test_roleAdd():
    token = getToken('admin')
    res = callAPI('put', f'/role/add?token={token}&roleTitle=TestRole&appTitle=Test&description=Some Description')
    parsed = res.json()
    assert res.ok
    assert isinstance(parsed, list)
    assert isinstance(parsed[0], int)
    res = callAPI('get', f'/role/get?token={token}&appTitle=Test&roleTitle=TestRole')
    parsed = res.json()
    assert res.ok
    assert parsed[1] == 'TestRole'
    assert parsed[2] == 'Some Description'

    token = getToken('default')
    res = callAPI('put', f'/role/add?token={token}&appTitle=Test&roleTitle=TestRole&description=Some Description')
    assert not res.ok
    assert res.status_code == 401

"""Updates a role"""
def test_roleUpdate():
    token = getToken('admin')
    res = callAPI('post', f'/role/update?token={token}&roleTitle=TestRole&appTitle=Test&description=New Description')
    parsed = res.json()
    assert res.ok
    assert parsed == 'Success'
    res = callAPI('get', f'/role/get?token={token}&roleTitle=TestRole&appTitle=Test')
    parsed = res.json()
    assert res.ok
    assert parsed[2] == 'New Description'

    token = getToken('default')
    res = callAPI('post', f'/role/update?token={token}&roleTitle=TestRole&appTitle=Test&description=New Description')
    assert not res.ok
    assert res.status_code == 401

"""Role/route list"""
def test_roleRouteList():
    ad_roles = [
        ['get', 'system/application/list'],
        ['get', 'system/application/get'],
        ['put', 'system/application/add'],
        ['delete', 'system/application/delete'],
        ['put', 'system/database/create'],
        ['get', 'system/database/list'],
        ['delete', 'system/database/delete'],
        ['get', 'system/role/list'],
    ]
    def_roles = [
        ['post', 'system/user/changeName'],
        ['post', 'system/user/changePassword'],
    ]
    token = getToken('admin')
    res = callAPI('get', f'/role/route/list?token={token}&roleTitle=Admin&appTitle=System')
    parsed = res.json()
    assert res.ok
    for role in ad_roles:
        assert role in parsed
    for role in def_roles:
        assert role in parsed
    res = callAPI('get', f'/role/route/list?token={token}&roleTitle=Default&appTitle=System')
    parsed = res.json()
    assert res.ok
    for role in ad_roles:
        assert role not in parsed
    for role in def_roles:
        assert role in parsed
    
    token = getToken('default')
    res = callAPI('get', f'/role/route/list?token={token}&roleTitle=Admin&appTitle=System')
    assert not res.ok
    assert res.status_code == 401

"""Bind a route to a role"""
def test_roleBind():
    token = getToken('admin')
    res = callAPI('put', f'/role/route/bind?token={token}&roleTitle=TestRole&appTitle=Test&operation=get&routeName=system/example')
    parsed = res.json()
    assert res.ok
    assert parsed == "Success"
    res = callAPI('get', f'/role/route/list?token={token}&roleTitle=TestRole&appTitle=Test')
    parsed = res.json()
    assert ['get', 'system/example'] in parsed

    token = getToken('default')
    res = callAPI('put', f'/role/route/bind?token={token}&roleTitle=TestRole&appTitle=Test&operation=get&routeName=system/example')
    assert not res.ok
    assert res.status_code == 401

"""Delete route errors when attached to a role"""
def test_roleRouteDeleteError():
    token = getToken('admin')
    res = callAPI('delete', f'/role/route/delete?token={token}&operation=get&routeName=system/example')
    assert not res.ok
    assert res.status_code == 500

    token = getToken('default')
    res = callAPI('delete', f'/role/route/delete?token={token}&operation=get&routeName=system/example')
    assert not res.ok
    assert res.status_code == 401

"""Unbind role test"""
def test_roleUnbind():
    token = getToken('admin')
    res = callAPI('delete', f'/role/route/unbind?token={token}&roleTitle=TestRole&appTitle=Test&operation=get&routeName=system/example')
    parsed = res.json()
    assert res.ok
    assert parsed == "Success"

    token = getToken('default')
    res = callAPI('delete', f'/role/route/unbind?token={token}&roleTitle=TestRole&appTitle=Test&operation=get&routeName=system/example')
    assert not res.ok
    assert res.status_code == 401

"""Deletes the unbound route"""
def test_roleRouteDeleteSuccess():
    token = getToken('admin')
    res = callAPI('delete', f'/role/route/delete?token={token}&operation=get&routeName=system/example')
    parsed = res.json()
    assert res.ok
    assert parsed == "Success"
    res = callAPI('get', f'/role/route/list?token={token}&appTitle=Test&roleTitle=TestRole')
    parsed = res.json()
    assert ['get', 'system/example'] not in parsed

    token = getToken('default')
    res = callAPI('delete', f'/role/route/delete?token={token}&operation=get&routeName=system/example')
    assert not res.ok
    assert res.status_code == 401

"""Add a user"""
def test_addUser():
    token = getToken('admin')
    res = callAPI('put', f'/user/add?token={token}&username=testnew&password=somepassword&name=Some Name')
    parsed = res.json()
    assert res.ok
    assert parsed == ['Success']
    res = callAPI('get', f'/user/list/all?token={token}')
    parsed = res.json()
    containsNew = False
    for user in parsed:
        if 'testnew' == user[1]:
            containsNew = True
    assert containsNew

    token = getToken('default')
    res = callAPI('put', f'/user/add?token={token}&username=testnew&password=somepassword&name=Some Name')
    assert not res.ok
    assert res.status_code == 401

"""Get new user token"""
def test_newUserToken():
    res = callAPI('post', f'/token?username=testnew&password=somepassword&appTitle=System')
    parsed = res.json()
    data = jwt.decode(parsed, os.getenv('SECRET'), algorithms=os.getenv('ALGORITHM'))
    assert data['sub'] == 'testnew'
    assert data['iss'] == 'System'

"""Change new user password"""
def test_newUserChangePassword():
    res = callAPI('post', f'/token?username=testnew&password=somepassword&appTitle=System')
    token = res.json()
    res = callAPI('post', f'/user/changePassword?token={token}&oldpass=somepassword&newpass=someotherpassword')
    parsed = res.json()
    assert res.ok
    assert parsed == 'Success'

    res = callAPI('post', f'/token?username=testnew&password=someotherpassword&appTitle=System')
    parsed = res.json()
    data = jwt.decode(parsed, os.getenv('SECRET'), algorithms=os.getenv('ALGORITHM'))
    assert data['sub'] == 'testnew'
    assert data['iss'] == 'System'

    res = callAPI('post', f'/token?username=testnew&password=somepassword&appTitle=System')
    parsed = res.json()
    assert not res.ok
    assert res.status_code == 500

"""Changes User Name"""
def test_changeName():
    res = callAPI('post', f'/token?username=testnew&password=someotherpassword&appTitle=System')
    token = res.json()
    res = callAPI('post', f'/user/changeName?token={token}&name=New%20Name')
    parsed = res.json()
    assert res.ok
    assert parsed == 'Success'

    token = getToken('admin')
    res = callAPI('get', f'/user/list/all?token={token}')
    parsed = res.json()
    flag = False
    for user in parsed:
        if user[1] == 'testnew' and user[3] == 'New Name':
            flag = True
    assert flag

"""Change expiration"""
def test_changeExpiration():
    token = getToken('admin')
    res = callAPI('post', f'/user/changeExpiration?token={token}&username=testnew&minutes=30')
    parsed = res.json()
    assert res.ok
    assert parsed == 'Success'
    res = callAPI('get', f'/user/list/all?token={token}')
    parsed = res.json()
    flag = False
    for user in parsed:
        if user[1] == 'testnew' and user[4] == 30:
            flag = True
    assert flag

    token = getToken('default')
    res = callAPI('post', f'/user/changeExpiration?token={token}&username=testnew&minutes=30')
    assert not res.ok
    assert res.status_code == 401

"""Registers a user for an application"""
def test_userRegisterApp():
    token = getToken('admin')
    res = callAPI('put', f'/user/register/app?token={token}&appTitle=Test&roleTitle=TestRole&appData=null&username=testnew')
    parsed = res.json()
    assert res.ok
    assert parsed == 'Success'
    res = callAPI('get', f'/user/list/app?token={token}&appTitle=Test')

    token = getToken('default')
    res = callAPI('put', f'/user/register/app?token={token}&appTitle=Test&roleTitle=TestRole&appData=null&username=testnew')
    assert not res.ok
    assert res.status_code == 401

"""List users by app"""
def test_userAppList():
    token = getToken('admin')
    res = callAPI('get', f'/user/list/app?token={token}&appTitle=Test')
    parsed = res.json()
    assert res.ok
    assert len(parsed) == 1
    assert parsed[0][1] == 'testnew'

    token = getToken('default')
    res = callAPI('get', f'/user/list/app?token={token}&appTitle=Test')
    assert not res.ok
    assert res.status_code == 401

"""List users by role"""
def test_userRoleList():
    token = getToken('admin')
    res = callAPI('get', f'/user/list/role?token={token}&appTitle=System&roleTitle=Admin')
    parsed = res.json()
    assert res.ok
    assert len(parsed) >= 2
    flag1 = False
    flag2 = False
    flag3 = True
    for user in parsed:
        if user[1] == 'admin':
            flag1 = True
        if user[1] == 'testsoftware':
            flag2 = True
        if user[2] == 'testsoftwaredefault':
            flag3 = False
    assert flag1 #Admin is present
    assert flag2 #testsoftware admin is present
    assert flag3 #default role testsoftware is not present

    token = getToken('default')
    res = callAPI('get', f'/user/list/role?token={token}&appTitle=System&roleTitle=Admin')
    assert not res.ok
    assert res.status_code == 401

"""List all users"""
def test_userListAll():
    token = getToken('admin')
    res = callAPI('get', f'/user/list/all?token={token}')
    parsed = res.json()
    assert res.ok
    assert len(parsed) >= 4 #admin and two test softwares should always be present. We also created an account so four should be the minimum
    flag1 = False
    flag2 = False
    flag3 = False
    flag4 = False
    for user in parsed:
        if user[1] == 'admin':
            flag1 = True
        if user[1] == 'testsoftware':
            flag2 = True
        if user[1] == 'testsoftwaredefault':
            flag3 = True
        if user[1] == 'testnew':
            flag4 = True
    assert flag1
    assert flag2
    assert flag3
    assert flag4
    
    token = getToken('default')
    res = callAPI('get', f'/user/list/all?token={token}')
    assert not res.ok
    assert res.status_code == 401

"""Removes user from application"""
def test_userLeaveApp():
    token = getToken('admin')
    res = callAPI('delete', f'/user/register/leaveApp?token={token}&appTitle=Test&username=testnew')
    parsed = res.json()
    assert res.ok
    assert parsed == 'Success'

    token = getToken('default')
    res = callAPI('delete', f'/user/register/leaveApp?token={token}&appTitle=Test&username=testnew')
    assert not res.ok
    assert res.status_code == 401

"""Deletes a user"""
def test_deleteUser():
    token = getToken('admin')
    res = callAPI('delete', f'/user/delete?token={token}&username=testnew')
    parsed = res.json()
    assert res.ok
    assert parsed == 'Success'

    token = getToken('default')
    res = callAPI('delete', f'/user/delete?token={token}&username=testnew')
    assert not res.ok
    assert res.status_code == 401

"""Delete a role"""
def test_roleDelete():
    token = getToken('admin')
    res = callAPI('delete', f'/role/delete?token={token}&roleTitle=TestRole&appTitle=Test')
    parsed = res.json()
    assert res.ok
    assert parsed == 'Successful'
    res = callAPI('get', f'/role/list?token={token}&appTitle=Test')
    parsed = res.json()
    assert ['TestRole'] not in parsed

    token = getToken('default')
    res = callAPI('delete', f'/role/delete?token={token}&roleTitle=TestRole&appTitle=Test')
    assert not res.ok
    assert res.status_code == 401

"""Delete application"""
def test_applicationDelete():
    token = getToken('admin')
    res = callAPI('delete', f'/application/delete?token={token}&title=Test')
    parsed = res.json()
    assert res.ok
    assert parsed == "Operation Successful"

    token = getToken('default')
    res = callAPI('delete', f'/application/delete?token={token}&title=Test')
    assert not res.ok
    assert res.status_code == 401

"""Remove Testing accounts"""
def test_removeTestingAccounts():
    res = callAPI('post', '/token?username=admin&password=password&appTitle=System')
    token = res.json()
    callAPI('delete', f'/user/delete?token={token}&username=testsoftware')
    callAPI('delete', f'/user/delete?token={token}&username=testsoftwaredefault')