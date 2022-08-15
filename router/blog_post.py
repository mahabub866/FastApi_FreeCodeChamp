from enum import Enum
from fastapi import APIRouter, status, Response, Query, Body, Path
from typing import List, Optional, Union
from pydantic import BaseModel

router = APIRouter(prefix='/blog', tags=['blog'])


class BlogModel(BaseModel):
    title: str
    content: str
    published: Optional[bool]
    nb_comment: int


@router.post('/new')
def create_blog(blog: BlogModel,):
    return {'data': blog}


@router.post('/new/{id}')
def create_blog(blog: BlogModel, id: int, version: int = 1):
    return {'data': blog, 'id': id, 'version': version

            }


@router.post('/new/{id}/comment/{comment_id}')
def create_comment(blog: BlogModel, id: int,
                   comment_title: str = Query(None, title='Id of the comment',
                                              description='Some description For  comment_id', alias='Comment_Title',
                                              deprecated=True),
                   content: str = Body(..., min_length=5,
                                       max_length=50, regex='^[a-z\s]*$'),
                   v: Optional[List[str]] = Query(['1.0', '1.1', '1.2']),
                   comment_id: int = Path(None, gt=5, le=10)
                   ):
    return {'blog': blog, 'id': id, 'comment_title': comment_title, 'content': content, 'version': v, 'comment_id': comment_id, }
