from enum import Enum
from fastapi import APIRouter, status, Response, Query, Body, Path,Depends,HTTPException
from typing import Dict, List, Optional, Union

from sqlalchemy.orm.session import Session
from db.database import get_db
from db import db_user
from db.hash import Hash
from db.models import DbUser
from schemas import SignUpModel, UserBase
from sqlalchemy import and_,or_

from fastapi.encoders import jsonable_encoder
router=APIRouter(
    prefix='/user',
    tags=['User']
)

# create
@router.post('/signup',response_model=SignUpModel)
async def create_user(request: SignUpModel, db: Session = Depends(get_db)):
    db_email = db.query(DbUser).filter(DbUser.email == request.email).first()
    if db_email is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'User with this email {request.email} Already Exists')

    db_username = db.query(DbUser).filter(
        DbUser.username == request.username).first()

    if db_username is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'User with this name {request.username} is Already Exists')
    
    db_counter_name = db.query(DbUser).filter(
        DbUser.counter_name == request.counter_name).first()

    if db_counter_name is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Counter {request.counter_name} is Already Exists')
    
    


    new_client = DbUser(username=request.username,
                            email=request.email,
                            password=Hash.bcrypt(request.password),
                            is_active=request.is_active,
                            counter_name=request.counter_name,
                            counter_no=request.counter_no,
                            counter_categories=request.counter_categories,
                            is_staff=request.is_staff,
                            )
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    response = {
            "username": new_client.username,
            "email": new_client.email,
            "password": new_client.password,
            "counter_name": new_client.counter_name,
            "counter_no": new_client.counter_no,
            "counter_categories": new_client.counter_categories,
            "is_active": new_client.is_active,
            "is_staff": new_client.is_staff
        }

    return jsonable_encoder(response)



# read all user
# @router.get('/all',response_model=List[UserDisplay])
# def get_users(db:Session=Depends(get_db)):
#     return db_user.get_all_user(db)
    
# # read 5user or 10user
# @router.get('/specific-user',response_model=List[UserDisplay])
# def get_users_specific(page_num:int=1,page_size:int=5,db:Session=Depends(get_db)):
#     return db_user.get_specifi_user(db,page_num,page_size)

# # read one  user
# @router.get('/{id}',response_model=UserDisplay)
# def get_users(id:int,db:Session=Depends(get_db)):
#     return db_user.get_user(db,id)


# # update

# @router.post('/{id}/update')
# def update_users(id:int,request:UserBase,db:Session=Depends(get_db)):
#     return db_user.update_user(db,id,request)


# # delete

# @router.get('/delete/{id}',)
# def delete_users(id,db:Session=Depends(get_db)):
#    return db_user.delete_user(id,db)