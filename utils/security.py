import os
from dotenv import load_dotenv
import jwt, jwt.exceptions as ex
from datetime import datetime as dt, timedelta, timezone
from fastapi import HTTPException, status
from .dbConn import getConn

load_dotenv()

#Exceptions
unauthorized = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="You do not have permission to access this function"
)

admin_infringement = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You cannot remove priveleges from admin"
)

bad_credentials = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect Credentials"
)

def generateToken(username:str, minutes:int):
    data = {
        "iss": "SphereAPI",
        "sub": username,
        "exp": dt.now(timezone.utc) + timedelta(minutes=minutes),
        "iat": dt.now(timezone.utc),
    }

    secret = os.getenv('SECRET')
    algorithm = os.getenv('ALGORITHM')

    token = jwt.encode(data, secret, algorithm=algorithm)
    return token

def validateToken(token:str):

    secret = os.getenv('SECRET')
    algorithm = os.getenv('ALGORITHM')

    try:
        data = jwt.decode(token, secret, algorithms=[algorithm])
        return data
    except ex.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token Expired"
        )
    except ex.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token invalid"
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong"
        )
    
def validateRole(username:str, operation:str, route:str):
    with open('scripts/system/role/getByUsername.sql') as f:
        query = f.read()

    params = {
        "username":username
    }

    conn = getConn('system')

    with conn.cursor() as cur:
        cur.execute(query, params)
        res = cur.fetchall()

    conn.close()

    print(res)

    return (operation, route) in res
    