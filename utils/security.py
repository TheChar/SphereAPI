import os
from dotenv import load_dotenv
import jwt, jwt.exceptions as ex
from datetime import datetime as dt, timedelta, timezone
from fastapi import HTTPException, status

load_dotenv()

def generateToken(username:str, minutes:int, roles:list[str]):
    data = {
        "iss": "SphereAPI",
        "sub": username,
        "exp": dt.now(timezone.utc) + timedelta(minutes=minutes),
        "iat": dt.now(timezone.utc),
        "roles": roles
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