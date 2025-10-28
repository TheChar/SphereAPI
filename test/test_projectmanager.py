import requests
import pytest
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

baseurl = "http://localhost:8000/projectmanager"

def1ID = -1
def2ID = -1
orgID = -1

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
        case 'syspost':
            res = requests.post(baseurl.replace('projectmanager', 'system')+path)
        case 'sysput':
            res = requests.put(baseurl.replace('projectmanager', 'system')+path)
        case 'sysdel':
            res = requests.delete(baseurl.replace('projectmanager', 'system')+path)
        case _:
            raise Exception('Invalid Method type')
    return res

def getToken(type):
    if type == 'default':
        res = callAPI('syspost', '/token?username=pmtestsoftware&password=password&appTitle=Project Manager')
    elif type == 'default2':
        res = callAPI('syspost', '/token?username=pmtestsoftware2&password=password&appTitle=Project Manager')
    else: 
        res = callAPI('syspost', '/token')
    token = res.json()
    return token

"""Creates testing accounts"""
def test_pminit():
    global def1ID, def2ID
    res = callAPI('syspost', '/token?username=admin&password=password&appTitle=System')
    token = res.json()
    callAPI('sysput', f'/user/add?token={token}&username=pmtestsoftware&password=password&name=PM Test Software')
    callAPI('sysput', f'/user/add?token={token}&username=pmtestsoftware2&password=password&name=PM Test Software 2')
    res = callAPI('syspost', '/token?username=pmtestsoftware&password=password&appTitle=System')
    token = res.json()
    callAPI('put', f'/contributor/register?token={token}')
    res = callAPI('syspost', '/token?username=pmtestsoftware2&password=password&appTitle=System')
    token = res.json()
    callAPI('put', f'/contributor/register?token={token}')
    #Get test account IDs
    token = getToken('default')
    data = jwt.decode(token, os.getenv('SECRET'), os.getenv('ALGORITHM'))
    def1ID = data['appdata']['contributorID']
    token = getToken('default2')
    data = jwt.decode(token, os.getenv('SECRET'), os.getenv('ALGORITHM'))
    def2ID = data['appdata']['contributorID']

"""Creates an organization under user"""
def test_createOrganization():
    global orgID
    token = getToken('default')
    res = callAPI('put', f'/organization/create?token={token}&orgTitle=Test Organization')
    parsed = res.json()
    assert res.ok
    assert parsed == "Success"
    res = callAPI('get', f'/contributor/organization/list?token={token}')
    parsed = res.json()
    assert res.ok
    flag = False
    for org in parsed:
        if org['title'] == 'Test Organization' and org['ownername'] == 'PM Test Software':
            orgID = org['organizationid']
            assert org['acceptedinvite']
            flag = True
    assert flag

"""Test Invite system"""
def test_inviteToOrg():
    global def1ID, def2ID, orgID
    token = getToken('default')
    res = callAPI('put', f'/organization/invite?token={token}&orgID={orgID}&newContID={def2ID}')
    parsed = res.json()
    assert res.ok
    assert parsed == "Success"
    token = getToken('default2')
    res = callAPI('get', f'/contributor/organization/list?token={token}')
    parsed = res.json()
    assert res.ok
    assert isinstance(parsed, list)
    for org in parsed:
        if org['organizationid'] == orgID:
            assert not org['acceptedinvite']

"""Test Join system"""
def test_joinOrg():
    global orgID
    token = getToken('default2')
    res = callAPI('put', f'/contributor/organization/join?token={token}&orgID={orgID}')
    parsed = res.json()
    assert res.ok
    assert parsed == 'Success'
    res = callAPI('get', f'/contributor/organization/list?token={token}')
    parsed = res.json()
    assert res.ok
    assert isinstance(parsed, list)
    for org in parsed:
        if org['organizationid'] == orgID:
            assert org['acceptedinvite']

"""Test leave org system"""
def test_leaveOrg():
    global orgID
    token = getToken('default2')
    res = callAPI('delete', f'/contributor/organization/leave?token={token}&orgTitle=Test Organization')
    parsed = res.json()
    assert res.ok
    assert parsed == 'Success'
    res = callAPI('get', f'/contributor/organization/list?token={token}')
    parsed = res.json()
    assert res.ok
    assert isinstance(parsed, list)
    flag = True
    for org in parsed:
        if org['title'] == 'Test Organization':
            flag = False
    assert flag

"""User cannot leave an organization they own"""
def test_noLeaveOrg():
    token = getToken('default')
    res = callAPI('delete', f'/contributor/organization/leave?token={token}&orgTitle=Test Organization')
    assert not res.ok

"""Org transfer fails to non-org member"""
def test_noNonMemberTransfer():
    global orgID, def2ID
    token = getToken('default')
    res = callAPI('post', f'/organization/transfer?token={token}&orgID={orgID}&newOwnerContID={def2ID}')
    assert not res.ok

"""Org transfer to org member"""
def test_OrgTransfer():
    global orgID, def2ID
    token = getToken('default')
    res = callAPI('put', f'/organization/invite?token={token}&orgID={orgID}&newContID={def2ID}')
    parsed = res.json()
    assert res.ok
    assert parsed == "Success"
    token = getToken('default2')
    res = callAPI('put', f'/contributor/organization/join?token={token}&orgID={orgID}')
    parsed = res.json()
    assert res.ok
    assert parsed == 'Success'
    token = getToken('default')
    res = callAPI('post', f'/organization/transfer?token={token}&orgID={orgID}&newOwnerContID={def2ID}')
    parsed = res.json()
    assert res.ok
    assert parsed == 'Success'
    res = callAPI('get', f'/contributor/organization/list?token={token}')
    parsed = res.json()
    for org in parsed:
        if org['organizationid'] == orgID:
            assert org['ownerid'] == def2ID

"""Dissolves an organization owned by user"""
def test_dissolveOrganization():
    token = getToken('default2')
    res = callAPI('delete', f'/organization/dissolve?token={token}&orgTitle=Test Organization')
    parsed = res.json()
    assert res.ok
    assert parsed == "Success"
    res = callAPI('get', f'/contributor/organization/list?token={token}')
    parsed = res.json()
    assert res.ok
    flag = True
    for org in parsed:
        if org['title'] == 'Test Organization' and org['ownername'] == 'PM Test Software':
            flag = False
    assert flag

"""Remove Testing accounts"""
def test_removeTestingAccounts():
    token = getToken('default')
    res = callAPI('delete', f'/contributor/leave?token={token}')
    parsed = res.json()
    assert res.ok
    assert parsed == 'Success'
    token = getToken('default2')
    res = callAPI('delete', f'/contributor/leave?token={token}')
    parsed = res.json()
    assert res.ok
    assert parsed == 'Success'
    res = callAPI('syspost', '/token?username=admin&password=password&appTitle=System')
    token = res.json()
    res = callAPI('sysdel', f'/user/delete?token={token}&username=pmtestsoftware')
    assert res.ok
    res = callAPI('sysdel', f'/user/delete?token={token}&username=pmtestsoftware2')
    assert res.ok