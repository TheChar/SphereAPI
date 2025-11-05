import requests
import pytest
import jwt
import os
from dotenv import load_dotenv
from datetime import datetime as dt, timezone
from urllib.parse import quote

load_dotenv()

baseurl = "http://localhost:8000/projectmanager"

def1ID = -1
def2ID = -1
def3ID = -1
orgID = -1
projectID = -1
tagID = -1
timeEntryID = -1

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
    elif type == 'default3':
        res = callAPI('syspost', '/token?username=pmtestsoftware3&password=password&appTitle=Project Manager')
    else: 
        res = callAPI('syspost', '/token')
    token = res.json()
    return token

"""Creates testing accounts"""
def test_pminit():
    global def1ID, def2ID, def3ID
    res = callAPI('syspost', '/token?username=admin&password=password&appTitle=System')
    token = res.json()
    callAPI('sysput', f'/user/add?token={token}&username=pmtestsoftware&password=password&name=PM Test Software')
    callAPI('sysput', f'/user/add?token={token}&username=pmtestsoftware2&password=password&name=PM Test Software 2')
    callAPI('sysput', f'/user/add?token={token}&username=pmtestsoftware3&password=password&name=PM Test Software 3')
    res = callAPI('syspost', '/token?username=pmtestsoftware&password=password&appTitle=System')
    token = res.json()
    callAPI('put', f'/contributor/register?token={token}')
    res = callAPI('syspost', '/token?username=pmtestsoftware2&password=password&appTitle=System')
    token = res.json()
    callAPI('put', f'/contributor/register?token={token}')
    res = callAPI('syspost', '/token?username=pmtestsoftware3&password=password&appTitle=System')
    token = res.json()
    callAPI('put', f'/contributor/register?token={token}')
    #Get test account IDs
    token = getToken('default')
    data = jwt.decode(token, os.getenv('SECRET'), os.getenv('ALGORITHM'))
    def1ID = data['appdata']['contributorID']
    token = getToken('default2')
    data = jwt.decode(token, os.getenv('SECRET'), os.getenv('ALGORITHM'))
    def2ID = data['appdata']['contributorID']
    token = getToken('default3')
    data = jwt.decode(token, os.getenv('SECRET'), os.getenv('ALGORITHM'))
    def3ID = data['appdata']['contributorID']

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

"""Create a tag"""
def test_createTag():
    global tagID, def1ID
    token = getToken('default')
    res = callAPI('put', f'/tag/create?token={token}&title=github-url&implements={{"url":"https://github.com/%path:str:%.git"}}&isPublic=true')
    parsed = res.json()
    assert res.ok
    assert parsed == 'Success'
    res = callAPI('get', f'/tag/list/byowner?token={token}&ownerID={def1ID}')
    parsed = res.json()
    assert res.ok
    assert isinstance(parsed, list)
    flag = False
    for tag in parsed:
        if tag['title'] == 'github-url':
            flag = True
            tagID = tag['tagid']
    assert flag

"""No illegal implementation syntax"""
def test_noBadTagImplementationSyntax():
    token = getToken('default')
    res = callAPI('put', f'/tag/create?token={token}&title=bad-tag&implements:{{"htrchg"}}&isPublic=true')
    assert not res.ok

"""No titles with spaces"""
def test_noBadTagTitleSyntax():
    token = getToken('default')
    res = callAPI('put', f'/tag/create?token={token}&title=Title With spaces&implements={{}}&isPublic=true')
    assert not res.ok

"""No public other than true false"""
def test_noBadTagPublicitySyntax():
    token = getToken('default')
    res = callAPI('put', f'/tag/create?token={token}&title=favorite-color&implements={{"color":"rgb(%red:int:0-255%, %green:num:0-255%, %blue:num:0-255%)"}}&isPublic=idk')
    assert not res.ok

"""Update a tag"""
def test_updateTag():
    global tagID
    token = getToken('default')
    res = callAPI('post', f'/tag/update?token={token}&tagID={tagID}&title=New Title&implements={{}}&isPublic=false')
    parsed = res.json()
    assert res.ok
    assert parsed == 'Success'
    res = callAPI('get', f'/tag/get?token={token}&tagID={tagID}')
    parsed = res.json()[0]
    assert isinstance(parsed, dict)
    assert parsed['title'] == 'New Title'
    assert parsed['implements'] == {}
    assert parsed['ispublic'] == False

"""List tags (considering public scope, owner, projects, etc.)"""
def test_noPrivateTagInList():
    global tagID
    token = getToken('default2')
    res = callAPI('get', f'/tag/list/all?token={token}&page=1')
    parsed = res.json()
    assert res.ok
    assert isinstance(parsed, list)
    flag = True
    for tag in parsed:
        if tag['tagid'] == tagID:
            flag = False
    assert flag

def test_PublicTagInList():
    global tagID
    token = getToken('default')
    res = callAPI('post', f'/tag/update?token={token}&tagID={tagID}&title=github-url&implements={{"url":"https://github.com/%path:str:%.git"}}&isPublic=true')
    assert res.ok
    token = getToken('default2')
    res = callAPI('get', f'/tag/list/all?token={token}&page=1')
    parsed = res.json()
    assert res.ok
    assert isinstance(parsed, list)
    flag = False
    for tag in parsed:
        if tag['tagid'] == tagID:
            flag = True
    assert flag

"""Create a project"""
def test_createProject():
    global projectID
    token = getToken('default')
    res = callAPI('put', f'/project/create?token={token}&title=Test Project&description=This is a test project&version=0.0.0a')
    parsed = res.json()
    assert res.ok
    assert parsed == 'Success'
    res = callAPI('get', f'/project/list/byowner?token={token}')
    parsed = res.json()
    assert res.ok
    assert isinstance(parsed, list)
    flag = False
    for project in parsed:
        if project['title'] == 'Test Project':
            flag = True
            projectID = project['projectid']
    assert flag

"""Update a project"""
def test_updateProject():
    global projectID
    token = getToken('default')
    res = callAPI('post', f'/project/update?token={token}&projectID={projectID}&title=New Title&description=New description&version=1.0.0b')
    parsed = res.json()
    assert res.ok
    assert parsed == 'Success'
    res = callAPI('get', f'/project/get?token={token}&projectID={projectID}')
    parsed = res.json()[0]
    assert res.ok
    assert isinstance(parsed, dict)
    assert parsed['projectid'] == projectID
    assert parsed['title'] == 'New Title'
    assert parsed['description'] == 'New description'
    assert parsed['version'] == '1.0.0b'
    assert parsed['ownerid'] == def1ID
    assert def1ID in parsed['contributorids']

"""Update one aspect of a project"""
def test_updateOneAspectProject():
    global projectID
    token = getToken('default')
    res = callAPI('post', f'/project/update?token={token}&projectID={projectID}&title=Another New Title&description=&version=')
    parsed = res.json()
    assert res.ok
    assert parsed == 'Success'
    res = callAPI('get', f'/project/get?token={token}&projectID={projectID}')
    parsed = res.json()[0]
    assert res.ok
    assert isinstance(parsed, dict)
    assert parsed['title'] == 'Another New Title'
    assert parsed['description'] == 'New description'
    assert parsed['numtimeentries'] == 4 #One for creating, one for joining, and two for updating (in this test and the previous one)

"""User who doesn't contribute can't update"""
def test_noUnauthorizedUpdate():
    global projectID
    token = getToken('default2')
    res = callAPI('post', f'/project/update?token={token}&projectID={projectID}&title=&description=&version=')
    assert not res.ok

"""Transfer of project doesn't work for non-contributors"""
def test_noTransferForNonContributor():
    global projectID, def2ID
    token = getToken('default')
    res = callAPI('post', f'/project/transfer?token={token}&projectID={projectID}&newOwnerID={def2ID}')
    assert not res.ok

"""Add project contributor doesn't work for non-contributors"""
def test_noUnauthorizedNewContributors():
    global projectID, def3ID
    token = getToken('default2')
    res = callAPI('put', f'/project/contributor/add?token={token}&projectID={projectID}&newContributorID={def3ID}')
    assert not res.ok

"""Test add project contributor"""
def test_addProjectContributor():
    global projectID, def2ID
    token = getToken('default')
    res = callAPI('put', f'/project/contributor/add?token={token}&projectID={projectID}&newContributorID={def2ID}')
    parsed = res.json()
    assert res.ok
    assert parsed == 'Success'
    res = callAPI('get', f'/project/get?token={token}&projectID={projectID}')
    parsed = res.json()[0]
    assert res.ok
    assert isinstance(parsed, dict)
    assert def2ID in parsed['contributorids']

"""Test if a contributor non-owner can add contributors"""
def test_nonOwnerAddProjectContributor():
    global projectID, def3ID
    token = getToken('default2')
    res = callAPI('put', f'/project/contributor/add?token={token}&projectID={projectID}&newContributorID={def3ID}')
    parsed = res.json()
    assert res.ok
    assert parsed == 'Success'
    res = callAPI('get', f'/project/get?token={token}&projectID={projectID}')
    parsed = res.json()[0]
    assert res.ok
    assert isinstance(parsed, dict)
    assert def3ID in parsed['contributorids']

"""No unauthorized contributor removal"""
def test_noUnauthorizedContributorRemoval():
    global def1ID, def2ID, projectID
    token = getToken('default3')
    res = callAPI('post', f'/project/contributor/remove?token={token}&projectID={projectID}&removedContributorID={def1ID}')
    assert not res.ok
    res = callAPI('post', f'/project/contributor/remove?token={token}&projectID={projectID}&removedContributorID={def2ID}')
    assert not res.ok

"""No unauthorized project owner removal"""
def test_noUnauthorizedProjectOwnerRemoval():
    global def1ID, projectID
    token = getToken('default2')
    res = callAPI('post', f'/project/contributor/remove?token={token}&projectID={projectID}&removedConributorID={def1ID}')
    assert not res.ok

"""No unauthorized contributor removal"""
def test_noUnauthorizedProjectContributorRemoval():
    global def3ID, projectID
    token = getToken('default2')
    res = callAPI('post', f'/project/contributor/remove?token={token}?projectID={projectID}&removedContributorID={def3ID}')
    assert not res.ok

"""Test removal of project contributor"""
def test_projectContributorRemoval():
    global def3ID, projectID
    token = getToken('default')
    res = callAPI('post', f'/project/contributor/remove?token={token}&projectID={projectID}&removedContributorID={def3ID}')
    parsed = res.json()
    assert res.ok
    assert parsed == 'Success'
    res = callAPI('get', f'/project/get?token={token}&projectID={projectID}')
    parsed = res.json()[0]
    assert res.ok
    assert isinstance(parsed, dict)
    token = getToken('default3')
    res = callAPI('get', f'/project/list/all?token={token}')
    parsed = res.json()
    assert res.ok
    assert isinstance(parsed, list)
    flag = True
    for project in parsed:
        if project['projectid'] == projectID:
            flag = False
    assert flag

"""Test normal contributor cannot restore removed"""
def test_noUnauthorizedRestore():
    global projectID, def3ID
    token = getToken('default2')
    res = callAPI('post', f'/project/contributor/restore?token={token}&projectID={projectID}&restoredContributorID={def3ID}')
    assert not res.ok

"""Test owner can restore removed"""
def test_restoreRemoved():
    global projectID, def3ID
    token = getToken('default')
    res = callAPI('post', f'/project/contributor/restore?token={token}&projectID={projectID}&restoredContributorID={def3ID}')
    parsed = res.json()
    assert res.ok
    assert parsed == 'Success'
    token = getToken('default3')
    res = callAPI('get', f'/project/list/all?token={token}')
    parsed = res.json()
    assert res.ok
    assert isinstance(parsed, list)
    flag = False
    for project in parsed:
        if project['projectid'] == projectID:
            flag = True
    assert flag

"""Tag not in project yet"""
def test_noTagInProject():
    global tagID, projectID
    token = getToken('default')
    res = callAPI('get', f'/tag/list/byproject?token={token}&projectID={projectID}')
    parsed = res.json()
    assert res.ok
    assert isinstance(parsed, list)
    flag = True
    for tag in parsed:
        if tag['tagid'] == tagID:
            flag = False
    assert flag

"""Project binds a tag by any contributor"""
def test_bindPublicTagByContributor():
    global tagID, projectID
    token = getToken('default3')
    res = callAPI('put', f'/project/tag/bind?token={token}&projectID={projectID}&tagID={tagID}&implementations={{"url":{{"path":"TheChar/projectmanager"}}}}')
    parsed = res.json()
    assert res.ok
    assert parsed == 'Success'
    res = callAPI('get', f'/project/tag/get?token={token}&projectID={projectID}&tagID={tagID}')
    assert res.ok
    parsed = res.json()[0]
    assert isinstance(parsed, dict)
    assert parsed['tagid'] == tagID
    assert parsed['projectid'] == projectID
    assert parsed['implementations'] == {"url":{"path":"TheChar/projectmanager"}}

"""Project unbinds a tag by any contributor"""
def test_unbindTagByContributor():
    global tagID, projectID
    token = getToken('default3')
    res = callAPI('delete', f'/project/tag/unbind?token={token}&projectID={projectID}&tagID={tagID}')
    parsed = res.json()
    assert res.ok
    assert parsed == 'Success'
    res = callAPI('get', f'/tag/list/byproject?token={token}&projectID={projectID}')
    parsed = res.json()
    assert res.ok
    assert isinstance(parsed, list)
    flag = True
    for tag in parsed:
        if tag['tagid'] == tagID:
            flag = False
    assert flag

"""Any contributor can get the implementation of a tag"""
#Checked in test_bindPublicTagByContributor

"""Create a timeentry"""
def test_createTimeEntry():
    global projectID, timeEntryID
    token = getToken('default')
    res = callAPI('put', f'/timeentry/create?token={token}&projectID={projectID}&description=Working on testing&version=')
    parsed = res.json()
    assert res.ok
    assert parsed == 'Success'
    res = callAPI('get', f'/timeentry/list/bycontributor?token={token}')
    assert res.ok
    parsed = res.json()
    assert isinstance(parsed, list)
    print(parsed)
    target = parsed[0] #Get the most recent entry as the target
    assert target['projecttitle'] == 'Another New Title'
    assert target['description'] == 'Working on testing'
    assert target['version'] == '1.0.0b'
    assert target['endtime'] == None
    timeEntryID = target['timeentryid']

def test_noUpdateTimeEntryUnauthorized():
    global timeEntryID
    token = getToken('default2')
    res = callAPI('post', f'/timeentry/update?token={token}&timeEntryID={timeEntryID}&startTime=&endTime=&description=&version=')
    assert not res.ok

"""Update a timeentry"""
def test_updateTimeEntry():
    global timeEntryID, projectID
    token = getToken('default')
    now = dt.now(timezone.utc)
    res = callAPI('post', f'/timeentry/update?token={token}&timeEntryID={timeEntryID}&startTime=&endTime={quote(now.isoformat())}&description=Some new description&version=')
    assert res.ok
    parsed = res.json()
    assert parsed == 'Success'
    res = callAPI('get', f'/timeentry/list/byproject?token={token}&projectID={projectID}')
    assert res.ok
    parsed = res.json()
    assert isinstance(parsed, list)
    for te in parsed:
        if te['timeentryid'] == timeEntryID:
            assert dt.fromisoformat(te['endtime']) == now
            assert te['description'] == 'Some new description'
            assert te['version'] == '1.0.0b'

def test_noUnauthorizedTimeEntryDeletion():
    global timeEntryID
    token = getToken('default2')
    res = callAPI('delete', f'/timeentry/delete?token={token}&timeEntryID={timeEntryID}')
    assert not res.ok

"""Delete non-system time entries"""
def test_deleteTimeEntry():
    global timeEntryID
    token = getToken('default')
    res = callAPI('delete', f'/timeentry/delete?token={token}&timeEntryID={timeEntryID}')
    assert res.ok
    parsed = res.json()
    assert parsed == 'Success'
    flag = True
    res = callAPI('get', f'/timeentry/list/bycontributor?token={token}')
    assert res.ok
    parsed = res.json()
    assert isinstance(parsed, list)
    flag = True
    for te in parsed:
        if te['timeentryid'] == timeEntryID:
            flag = False
    assert flag

"""Delete a project"""
def test_deleteProject():
    global projectID
    token = getToken('default')
    res = callAPI('delete', f'/project/delete?token={token}&projectID={projectID}')
    parsed = res.json()
    assert res.ok
    assert parsed == 'Success'
    flag = True
    res = callAPI('get', f'/project/list/byowner?token={token}')
    parsed = res.json()
    assert res.ok
    assert isinstance(parsed, list)
    for project in parsed:
        if project['title'] == 'Test Project':
            flag = False
    assert flag

"""Delete a tag"""
def test_deleteTag():
    global tagID
    token = getToken('default')
    res = callAPI('delete', f'/tag/delete?token={token}&tagID={tagID}')
    parsed = res.json()
    assert res.ok
    assert parsed == 'Success'
    res = callAPI('get', f'/tag/get?token={token}&tagID={tagID}')
    assert not res.ok

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
    token = getToken('default3')
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
    res = callAPI('sysdel', f'/user/delete?token={token}&username=pmtestsoftware3')