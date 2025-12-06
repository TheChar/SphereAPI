"""
Routes: projectmanager/tag/* => create, update, list/byowner, list/byproject, list/all, get
"""

from fastapi import APIRouter
from ...utils.dbConn import getConn
from ...utils import security
from psycopg2.extras import DictCursor
import json
from datetime import datetime, timezone

app = "Project Manager"
db = 'projectmanager'
router = APIRouter(prefix='/tag')

def parse(impStr:str):
    queries = []
    split = impStr.split('%')
    types = ['str', 'float', 'int', 'char', 'bool', 'date', 'file']
    strConstraints = ['contains', 'minlen', 'maxlen']
    floatConstraints = ['decplaces', 'min', 'max']
    intConstraints = ['min', 'max']
    charConstraints = []
    boolConstraints = []
    dateConstraints = ['mindate', 'maxdate', 'format']
    fileConstraints = ['type', 'maxkb']
    for idx, item in enumerate(split):
        if idx % 2 != 0:
            queries.append(item)
    print(f'Collected the queries: {queries}')
    for query in queries:
        print(f'Working query: {query}')
        if not isinstance(query, str):
            raise Exception('Not valid syntax. Query cannot be parsed as string')
        try:
            if len(query) > 0:
                if ':' in query:
                    querySplit = query.split(':')
                    name = querySplit[0]
                    type = querySplit[1]
                    constraints = querySplit[2]
                    if constraints == '':
                        break
                    if type not in types:
                        raise Exception('Type is invalid')
                    splitConstraints = constraints.split(',')
                    match type:
                        case 'str':
                            for constraint in splitConstraints:
                                splitConstraint = constraint.split('=')
                                if splitConstraint[0] not in strConstraints:
                                    raise Exception(f'String constraint is invalid: {constraint}')
                                match splitConstraint[0]:
                                    case 'contains':
                                        try:
                                            str(splitConstraint[1])
                                        except:
                                            raise Exception(f'Contains value is not a string: contains={splitConstraint[1]}')
                                        break
                                    case 'minlen':
                                        try:
                                            int(splitConstraint[1])
                                        except:
                                            raise Exception(f'Minlen value is not an int: minlen={splitConstraint[1]}')
                                        break
                                    case 'maxlen':
                                        try:
                                            int(splitConstraint[1])
                                        except:
                                            raise Exception(f'Maxlen value is not an int: maxlen={splitConstraint[1]}')
                                        break
                        case 'float':
                            for constraint in splitConstraints:
                                splitConstraint = constraint.split('=')
                                if splitConstraint[0] not in floatConstraints:
                                    raise Exception(f'Float constraint is invalid: {constraint}')
                                match splitConstraint[0]:
                                    case 'decplaces':
                                        try:
                                            int(splitConstraint[1])
                                        except:
                                            raise Exception(f'Decplaces value is not an int: decplaces={splitConstraint[1]}')
                                        break
                                    case 'min':
                                        try:
                                            float(splitConstraint[1])
                                        except:
                                            raise Exception(f'Min value is not a float: min={splitConstraint[1]}')
                                        break
                                    case 'max':
                                        try:
                                            float(splitConstraint[1])
                                        except:
                                            raise Exception(f'Max value is not a float: max={splitConstraint[1]}')
                                        break
                        case 'int':
                            for constraint in splitConstraints:
                                splitConstraint = constraint.split('=')
                                if splitConstraint[0] not in intConstraints:
                                    raise Exception(f'Int constraint is invalid: {constraint}')
                                match splitConstraint[0]:
                                    case 'min':
                                        try:
                                            int(splitConstraint[1])
                                        except:
                                            raise Exception(f'Min value is not an integer: min={splitConstraint[1]}')
                                        break
                                    case 'max':
                                        try:
                                            int(splitConstraint[1])
                                        except:
                                            raise Exception(f'Max value is not an integer: max={splitConstraint[1]}')
                                        break
                        case 'char':
                            for constraint in splitConstraints:
                                splitConstraint = constraint.split('=')
                                if splitConstraint[0] not in charConstraints:
                                    raise Exception(f'Char constraint is invalid: {constraint}')
                        case 'bool':
                            for constraint in splitConstraints:
                                splitConstraint = constraint.split('=')
                                if splitConstraint[0] not in boolConstraints:
                                    raise Exception(f'Boolean constraint is invalid: {constraint}')
                        case 'date':
                            for constraint in splitConstraints:
                                splitConstraint = constraint.split('=')
                                if splitConstraint[0] not in dateConstraints:
                                    raise Exception(f'Date constraint is invalid: {constraint}')
                                match splitConstraint[0]:
                                    case 'mindate':
                                        try:
                                            datetime.strptime(splitConstraint[1])
                                        except:
                                            raise Exception(f'Mindate value is not of type date: mindate={splitConstraint[1]}')
                                        break
                                    case 'maxdate':
                                        try:
                                            datetime.strptime(splitConstraint[1])
                                        except:
                                            raise Exception(f'Maxdate value is not of type date: maxdate={splitConstraint[1]}')
                                        break
                                    case 'format':
                                        try:
                                            datetime.strftime(datetime.now(timezone.utc), splitConstraint[1])
                                        except:
                                            raise Exception(f'Format value is not a valid format: format={splitConstraint[1]}')
                        case 'file':
                            for constraint in splitConstraints:
                                splitConstraint = constraint.split('=')
                                if splitConstraint[0] not in fileConstraints:
                                    raise Exception(f'File constraint is invalid: {constraint}')
                                match splitConstraint[0]:
                                    case 'type':
                                        if not splitConstraint[0][0] == '.' and not splitConstraint[0][1:].isalnum():
                                            raise Exception(f'Type value is not a valid file extension: format={splitConstraint[1]}')
                                        break
                                    case 'maxkb':
                                        try:
                                            int(splitConstraint[1])
                                        except:
                                            raise Exception(f'Maxsize value is not an integer: maxkb={splitConstraint[1]}')
                else:
                    raise Exception(f'Not valid syntax. No : symbol found in query {query}')
            else:
                print('detected % symbol')
        except Exception as e:
            print(e)
            raise security.something_wrong

def validateImplementsSyntax(imp:str):
    try:
        jsonImp = json.loads(imp)
        if not isinstance(jsonImp, dict):
            raise Exception('Not a dictionary')
        for key, value in jsonImp.items():
            if not isinstance(value, str):
                raise Exception(f'Value of {key} was not a string')
            print(f'Parsing {value}')
            parse(value)
    except Exception as e:
        print(e)
        raise security.something_wrong

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
        print(f'Sending {implements} to validation pipeline')
        validateImplementsSyntax(implements)
        if ' ' in title:
            raise Exception('No spaces in titles')
        if not (isPublic == 'true' or isPublic == 'false'):
            raise Exception('isPublic must be true or false')
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
        "Title": title if title != '' else None,
        "Implements": implements if implements != '' else None,
        "TagID": tagID,
        "IsPublic": isPublic if (isPublic != '' and (isPublic == 'true' or isPublic == 'false')) else None
    }
    try:
        validateImplementsSyntax(implements)
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
async def listByOwner(token:str, ownerID:str=''):
    data = security.validateToken(token)
    if not security.validateRole(app, data['role'], 'get', 'projectmanager/tag/list/byowner'):
        raise security.unauthorized
    with open('scripts/projectmanager/tag/list/byowner.sql') as f:
        query = f.read()
        f.close()
    params = {
        "ContributorID": data['appdata']['contributorID'],
        "OwnerID": ownerID if ownerID != '' else data['appdata']['contributorID'] #If no owner id is given, collect tags owned by caller
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
async def getAllPublicTags(token:str, page:str, searchBy:str, sortBy:str): #TODO: A more secure method of passing in search queries is needed
    data = security.validateToken(token)
    if not security.validateRole(app, data['role'], 'get', 'projectmanager/tag/list/all'):
        raise security.unauthorized
    with open('scripts/projectmanager/tag/list/all.sql') as f:
        query = f.read()
        f.close()
    params = {
        "ContributorID": data['appdata']['contributorID'],
        "Page": page,
        "SearchBy": searchBy if searchBy != '' else None
    }
    match sortBy:
        case 'leastUses':
            query = query.replace('{ORDER_BY}', 'NumImplementations ASC')
        case 'mostUses':
            query = query.replace('{ORDER_BY}', 'NumImplementations DESC')
        case 'title':
            query = query.replace('{ORDER_BY}', 'T.Title ASC')
        case 'titleD':
            query = query.replace('{ORDER_BY}', 'T.Title DESC')
        case 'owner':
            query = query.replace('{ORDER_BY}', 'C.Name ASC')
        case 'ownerD':
            query = query.replace('{ORDER_BY}', 'C.Name DESC')
        case _:
            raise security.something_wrong
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