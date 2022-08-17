from datetime import timedelta
from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm.session import Session

from .oauth2 import create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES
from db.database import get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from db import models
from db.hash import Hash
router=APIRouter(
    tags=['Authentication']
)
@router.post('/token')
def get_token(request:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user=db.query(models.DbUser).filter(models.DbUser.username==request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Credintials Invalid ')
    if not Hash.verify(user.password,request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Password Invalid ')
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer",
    'user_id':user.id,'username':user.username},
