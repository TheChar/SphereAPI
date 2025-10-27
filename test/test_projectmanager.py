import requests
import pytest
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

baseurl = "http://localhost:8000/projectmanager"

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
    if type == 'default':
        res = callAPI('post', '/token?username=pmtestsoftware&password=password&appTitle=Project Manager')
    else: 
        res = callAPI('post', '/token')
    token = res.json()
    return token

"""Creates testing accounts"""
def test_pminit():
    res = callAPI('post', '/token?username=admin&password=password&appTitle=System')
    token = res.json()
    callAPI('put', f'/user/add?token={token}&username=pmtestsoftware&password=password&name=PM Test Software')
    res = callAPI('post', '/token?username=pmtestsoftware&password=password&appTitle=System')
    token = res.json()
    callAPI('put', f'/contributor/register?token={token}')

"""Creates an organization under user"""
def test_createOrganization():
    token = getToken('default')
    res = callAPI('put', f'/organization/create?token={token}&orgTitle=Test Organization')
    parsed = res.json()
    assert res.ok
    assert parsed == "Success"
    res = callAPI('get', f'/contributor/organization/list?token={token}')
    parsed = res.json()
    assert res.ok
    assert 

"""Remove Testing accounts"""
def test_removeTestingAccounts():
    res = callAPI('post', '/token?username=admin&password=password&appTitle=System')
    token = res.json()
    callAPI('delete', f'/user/delete?token={token}&username=pmtestsoftware')