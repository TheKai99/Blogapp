
from fastapi import Depends
import jwt
from src.utils.settings import settings
from src.utils.db import get_db
from fastapi import status , HTTPException
from sqlalchemy import select
from src.user.models import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login") 



async def get_current_user_id(token:str = Depends(oauth2_scheme) , db:AsyncSession = Depends(get_db)) -> int:

    try:
            payload = jwt.decode(token , settings.SECRET_KEY , algorithms=settings.ALGORITHM)
            print(payload)
            user_id = payload["_id"]
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="token expired")
        
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="invalid token")
    
    result = await db.execute(select(UserModel).where(UserModel.id == int(user_id)))
    is_user = result.scalar_one_or_none()
    
    if is_user is None:
        raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="User not found")
    
    return int(user_id)