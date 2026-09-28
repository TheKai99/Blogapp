from fastapi import HTTPException ,status
from sqlalchemy.orm import Session
from src.user.models import UserModel
from src.user.dtos import UserSchema




def create_user(data:UserSchema , db:Session):

    user_data = data.model_dump()

    is_user = db.query(UserModel).filter(UserModel.username == user_data["username"]).first()

    if is_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="username already exist cant make user")

    is_user = db.query(UserModel).filter(UserModel.email == user_data["email"]).first()

    if is_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="email already exist try with another")

    

    new_user = UserModel(
        username = user_data['username'],
        email = user_data['email'],
        image_file = user_data['image_file']


    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    

    return new_user


def get_user(user_id:int , db:Session):

    is_user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not is_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="user not exist")


    return is_user