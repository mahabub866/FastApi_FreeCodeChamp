from enum import Enum
from fastapi import APIRouter, status, Response, Query, Body, Path,Depends
from typing import Dict, List, Optional, Union

from sqlalchemy.orm.session import Session
from db.database import get_db
from db import db_article
from schemas import ArticleBase, ArticleDisplay, UserBase
from auth.oauth2 import get_current_user, oauth2_scheme

router=APIRouter(
    prefix='/article',
    tags=['Article']
)


# create
@router.post('/create',response_model=ArticleDisplay)
def create_articles(request:ArticleBase,db:Session=Depends(get_db)):
    return db_article.create_article(db,request)

# read one  article
@router.get('/{id}')#,response_model=ArticleDisplay)
def get_articles(id:int,db:Session=Depends(get_db),current_user:UserBase=Depends(get_current_user)):
    return {'data':db_article.get_article(db,id),
    'current_user':current_user}


    # read all article
# @router.get('/all',response_model=List[ArticleDisplay])
# def get_articles(db:Session=Depends(get_db)):
#     return db_article.get_article_s(db)
    
# # read 5article or 10article
# @router.get('/specific-article',response_model=List[ArticleDisplay])
# def get_article_specific(page_num:int=1,page_size:int=5,db:Session=Depends(get_db)):
#     return db_article.get_specifi_article(db,page_num,page_size)



# # update

# @router.post('/{id}/update')
# def update_articles(id:int,request:ArticleBase,db:Session=Depends(get_db)):
#     return db_article.update_article(db,id,request)


# # delete

# @router.get('/delete/{id}',)
# def delete_articles(id,db:Session=Depends(get_db)):
#    return db_article.delete_article(id,db)
