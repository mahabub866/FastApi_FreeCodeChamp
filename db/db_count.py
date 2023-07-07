
from fastapi import HTTPException,status
from sqlalchemy.orm.session import Session
from db.models import DbArticle
from exceptions import StoryException
from schemas import ArticleBase


def create_article(db: Session, request: ArticleBase):
    if request.content.startswith('Once upon a time'):
        raise StoryException('No stories Pleas')
    new_article = DbArticle(title=request.title,
                            content=request.content, published=request.published, user_id=request.creator_id)
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article


def get_article(db: Session, id: int):
    article= db.query(DbArticle).filter(DbArticle.id == id).first()
    # error handling
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Article  with id {id} not Found')
    return article

# def get_article_s(db:Session,request:ArticleBase):
#     article=db.query(DbArticle).filter(DbArticle.id==id).first()
#     return article


# def get_specifi_article(db: Session, page_num: int, page_size: int):
#     start = (page_num-1)*page_size
#     end = start+page_size
#     return db.query(DbArticle)[start:end]


# def update_article(db: Session,id: int,request: ArticleBase ):
#     user = db.query(DbArticle).filter(DbArticle.id == id)
#     # user.update(request.dict())
#     user.update({DbArticle.username: request.username, DbArticle.email: request.email,
#                 })
#     db.commit()
#     return 'Updated Sucessufly'


# def delete_article(id:int,db:Session):
#     user=db.query(DbArticle).filter(DbArticle.id==id).first()
#     db.delete(user)
#     db.commit()
#     return 'Deleted Sucessufly'
