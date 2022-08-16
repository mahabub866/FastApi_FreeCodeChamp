
from sqlalchemy.orm.session import Session
from db.models import DbArticle
from schemas import ArticleBase


def create_article(db:Session,request:ArticleBase):
    new_article = DbArticle(title=request.title,
                      content=request.content,published=request.published )
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article
    

def get_article(db: Session, id: int):
    return db.query(DbArticle).filter(DbArticle.id == id).first()

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