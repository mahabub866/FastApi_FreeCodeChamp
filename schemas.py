
from datetime import datetime
from enum import Enum
from pydantic import BaseModel,validator,Field
from typing import  Optional
from datetime import timedelta
from fastapi import APIRouter, Depends, status, HTTPException


class TokenStatus(str, Enum):
    PROCESSING = 'PROCESSING'
    INTRANSIT = 'REJECT'
    HOLD = 'HOLD'
    DONE = 'DONE'
    # class Config():
    #     orm_mode=True

class CounterStatus(str, Enum):
    reg = 'reg'
    xray = 'xray'
    m_doctor = 'm_doctor'
    eye = 'eye'
    f_doctor = 'f_doctor'
    urin = 'urin'
    admin='admin'
    done='done'
    reject='reject'
    # class Config():
    #     orm_mode=True

class TokenModel(BaseModel):
    id:Optional[int]
    token_id:int
    token_status:TokenStatus
    t_counter_categories:CounterStatus
    reg:bool
    xray :bool
    m_doctor :bool
    f_doctor :bool
    eye :bool
    urin :bool
    registration_picked :bool
    is_picked :bool
    
    
class SignUpModel(BaseModel):
    id:Optional[int]
    username:str
    email:str
    counter_name:str=Field(regex='^Counter \d{1,2}$')
    counter_no:int
    password:str
    is_active:Optional[bool]
    is_staff:Optional[bool]
    counter_categories:CounterStatus
    class Config():
        orm_mode=True
        schema_extra={
            'example':{
                "username":"mahabub",
                "email":"mahabub@gmail.com",
                "password":'mahabub',
                "counter_name":"Counter 0",
                "counter_no":0,
                "counter_categories":"reg",
                "is_staff":False,
                "is_active":True,

            }
        }

class TokenIDModel(BaseModel):
    token_id:int
    

    class Config():
        orm_mode=True
        schema_extra={
            "example":{
                "token_id":2,
                 
            }
        }
class TokenStatusModel(BaseModel):
    token_status:TokenStatus
    

    class Config():
        orm_mode=True
        schema_extra={
            "example":{
                "token_status":"PROCESSING",
                 
            }
        }
class TokenCategoriesModel(BaseModel):
    t_counter_categories:str
    

    class Config():
        orm_mode=True
        schema_extra={
            "example":{
                "t_counter_categories":"reg",
                 
            }
        }

class TokenID(BaseModel):
    token_id:int
    class Config():
        orm_mode = True



class CounterDisplay(BaseModel):
    counter:int
    reg_token:TokenID
    

    class Config():
        orm_mode = True
class CounterActiveModel(BaseModel):
    is_active:bool
    

    class Config():
        orm_mode=True
        schema_extra={
            "example":{
                "is_active":True
                 
            }
        }

class CounterCategoriesModel(BaseModel):
    counter_categories:CounterStatus
    
    class Config():
        orm_mode=True
        schema_extra={
            "example":{
                "counter_categories":"xray",
                 
            }
        }

class Settings(BaseModel):
    AUTHJWT_SECRET_KEY:str='mahabubea305b1b472fc85371e27dec1997!'
    authjwt_access_token_expires: timedelta = timedelta(hours=15)
    authjwt_refresh_token_expires: timedelta = timedelta(days=30)
    

class LoginModel(BaseModel):
    username:str
    password:str


# async def jwt_auth(Authorize: AuthJWT = Depends()):
#     try:
#         Authorize.jwt_required()

#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")

#     username = Authorize.get_jwt_subject()
#     print(username)
#     return username

class UserBase(BaseModel):
    username:str
    email:str
    password:str
    
