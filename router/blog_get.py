from enum import Enum
from fastapi import APIRouter,status,Response,Depends
from typing import Optional, Union

from .blog_post import required_functionality

router=APIRouter(prefix='/blog',tags=['blog'])


@router.get("/all")
def get_all_blog(page=1, page_size: Optional[int] = None,req_parameter:dict=Depends(required_functionality)):
    return {"message": f"all {page_size} blogs on page {page}",'req':req_parameter}



@router.get("/{id}",status_code=status.HTTP_200_OK,
summary='Individual Blog',
description='This api Call individual id fetching data',
response_description='The list of availabe blog'
 )
def get_blog(id:int,response:Response):
    if id>5:
        response.status_code=status.HTTP_404_NOT_FOUND
        return {"error":f'blog {id} is not found'}
    else:
        response.status_code=status.HTTP_200_OK
        return {"message": f"blog {id} is found "}


@router.get("/{id}/comments/{comment_id}",tags=['comment'])
def get_comment(id: int, comment_id: int, valid: bool = True, username: Optional[str] = None):
    return {"message": f"blog_id {id} comment_id {comment_id} ,username {username} valid {valid}  "}


class BlogType(str, Enum):
    short = "short"
    long = "long"
    high = "high"


@router.get('/type/{type}')
def blog_type(type: BlogType):
    return {"message": f'blog type: {type}'}

