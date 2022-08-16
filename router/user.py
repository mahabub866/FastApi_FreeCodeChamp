from enum import Enum
from fastapi import APIRouter, status, Response, Query, Body, Path,Depends
from typing import Dict, List, Optional, Union

from sqlalchemy.orm.session import Session
from db.database import get_db
from db import db_user
from schemas import UserBase, UserDisplay

router=APIRouter(
    prefix='/user',
    tags=['User']
)

# create
@router.post('/create',response_model=UserDisplay)
def create_users(request:UserBase,db:Session=Depends(get_db)):
    return db_user.create_user(db,request)


# read all user
@router.get('/all',response_model=List[UserDisplay])
def get_users(db:Session=Depends(get_db)):
    return db_user.get_all_user(db)
    
# read 5user or 10user
@router.get('/specific-user',response_model=List[UserDisplay])
def get_users_specific(page_num:int=1,page_size:int=5,db:Session=Depends(get_db)):
    return db_user.get_specifi_user(db,page_num,page_size)

# read one  user
@router.get('/{id}',response_model=UserDisplay)
def get_users(id:int,db:Session=Depends(get_db)):
    return db_user.get_user(db,id)


# update

@router.post('/{id}/update')
def update_users(id:int,request:UserBase,db:Session=Depends(get_db)):
    return db_user.update_user(db,id,request)


# delete

@router.get('/delete/{id}',)
def delete_users(id,db:Session=Depends(get_db)):
   return db_user.delete_user(id,db)