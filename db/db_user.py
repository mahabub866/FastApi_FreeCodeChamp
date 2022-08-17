from sqlalchemy.orm.session import Session
from schemas import UserBase
from db.models import DbUser
from db.hash import Hash
from fastapi import HTTPException,status


def create_user(db: Session, request: UserBase):
    new_user = DbUser(username=request.username,
                      email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_all_user(db: Session):
    return db.query(DbUser).all()


def get_specifi_user(db: Session, page_num: int, page_size: int):
    start = (page_num-1)*page_size
    end = start+page_size
    return db.query(DbUser)[start:end]


def get_user_by_username(db: Session, username: str):
    user=db.query(DbUser).filter(DbUser.username == username).first()
    if not user: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'User  with username {username} not Found')
    return user

def get_user(db: Session, id: int):
    user=db.query(DbUser).filter(DbUser.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'User  with id {id} not Found')
    return user

def update_user(db: Session,id: int,request: UserBase ):
    user = db.query(DbUser).filter(DbUser.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'User  with id {id} not Found')
    # user.update(request.dict())
    user.update({DbUser.username: request.username, DbUser.email: request.email,
                DbUser.password: Hash.bcrypt(request.password)})
    db.commit()
    return 'Updated Sucessufly'


def delete_user(id:int,db:Session):
    user=db.query(DbUser).filter(DbUser.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'User  with id {id} not Found')
    # user.update(request.dict())
    db.delete(user)
    db.commit()
    return 'Deleted Sucessufly'