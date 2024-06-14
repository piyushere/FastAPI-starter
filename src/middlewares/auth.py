import jwt
from fastapi import Request, status
from fastapi.exceptions import HTTPException
from src.models.user import User
from datetime import timezone, timedelta, datetime


async def authorize(request: Request):
    token = request.cookies.get('auth_session')
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please login and try again",
        )
    try:
        user = jwt.decode(token, 'helloworld', algorithms=['HS256'])
        request.state.user = User.model_validate(user)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired, please login and try again",
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid/tampered auth token, please login and try again",
        )


def generate_token(attributes: dict):
    user = User(
        id=attributes.get('id')[0],
        email=attributes.get('email')[0],
        firstName=attributes.get('firstName')[0],
        lastName=attributes.get('lastName')[0]
    ).model_dump()
    user["exp"] = datetime.now(tz=timezone.utc) + timedelta(seconds=10)
    token = jwt.encode(user, 'helloworld')
    return token
