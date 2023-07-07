
from asyncio.windows_events import NULL
from datetime import datetime


import uuid

from fastapi import APIRouter, Depends,status,HTTPException

from sqlalchemy import and_

from sqlalchemy.orm import Session, load_only

from fastapi.encoders import jsonable_encoder
from db.database import get_db
from db.models import DbCount,DbToken, DbUser
import asyncio

from schemas import CounterActiveModel, CounterCategoriesModel


from schemas import UserBase
from auth.oauth2 import get_current_user, oauth2_scheme

count_router = APIRouter(
    prefix='/count',
    tags=['Count']
)

# create
@count_router.get('/create',status_code=status.HTTP_200_OK)
async def create_count( db: Session = Depends(get_db)):
    startDate = datetime.now()
    endDate = datetime.now()

    startDate = str(startDate.date()) + " 00:00:00"
    endDate = str(endDate.date()) + " 23:23:59"

    format = '%Y-%m-%d %H:%M:%S'

    

    is_exixt=  db.query(DbCount).filter( and_(DbCount.date >= datetime.strptime(startDate, format), DbCount.date <= datetime.strptime(endDate, format))  ).first()

    # print("ss",is_exixt)

    count = NULL

    if  is_exixt is None:
        new_receipt = DbCount( id = str(uuid.uuid4()))
        db.add(new_receipt)
        db.commit()
        db.refresh(new_receipt)
        
        count = 1

        db.query(DbToken).delete()
    
        db.commit()

    else:
        
        new_receipt = db.query(DbCount).filter(DbCount.id == is_exixt.id ).update({'count_no' : DbCount.count_no +1})
        db.commit()
        count = is_exixt.count_no

    # print (count)
    db_token=db.query(DbToken).filter(DbToken.token_id).all()
    lasttokenNo=len(db_token) or 0
    # print(lasttokenNo)
    new_token=DbToken(token_id=lasttokenNo+1,token_status="PROCESSING",t_counter_categories="reg",create_at=datetime.now())
    db.add(new_token)
    db.commit()
    db.refresh(new_token)
    return new_token.token_id

# read one  article

@count_router.get('/display/{counter_no}')
async def display(counter_no:int, db:Session=Depends(get_db)):


    # counter_no
    number = db.query(DbToken).filter(DbToken.counter == counter_no).first()
    
    if(number != None):
        return number.token_id
    else: 
        # return None
        return None

@count_router.get('/total/daily')
async def daily_total_count(db:Session=Depends(get_db)):


    # counter_no
    number = db.query(DbCount).all()
    
    return number

@count_router.get('/all/{status}')
async def display( status:str,db:Session=Depends(get_db)):

    # counter_no
    number = db.query(DbToken).filter(and_( DbToken.token_status == status , DbToken.is_picked == False) ).options(load_only(*['token_id', 't_counter_categories'])).all()

    return number

@count_router.get('/serving')
async def serving(db:Session=Depends(get_db)):

    # counter_no
    counter = db.query(DbUser).options(load_only(*['counter_no'])).all()
    data = []
    for i in counter: 

        tokenData = counter = db.query(DbToken).filter(and_(DbToken.counter == i.counter_no)).options(load_only(*['token_id'])).first()
        
        if(tokenData != None):
            data.append({ "counter" : i.counter_no, 'token_id' :  tokenData.token_id})

        else:
            data.append({ "counter" : i.counter_no, 'token_id' :  -1})

    # print(data)
    # DbUser.

    return data

@count_router.patch('/counter-active/{counter_name}')
async def counter_status(counter_name: str, counter_status: CounterActiveModel, current_user: UserBase = Depends(get_current_user),db: Session = Depends(get_db)):


    username = current_user

    current_user = db.query(DbUser).filter(DbUser.username == username).first()

    if current_user.is_staff and current_user.is_active:
        db_counter_name = db.query(DbUser).filter(
            DbUser.counter_name == counter_name).first()

        if db_counter_name is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Counter name {counter_name} doestn't Exists")

        status_to_update = db.query(DbUser).filter(
            DbUser.counter_name == counter_name).first()

        status_to_update.is_active = counter_status.is_active

        db.commit()

        response = {
                "id":status_to_update.id,
                "is_active":status_to_update.is_active,
                "username":status_to_update.username,
                "is_staff":status_to_update.is_staff,
                "counter_name":status_to_update.counter_name,
                "counter_no":status_to_update.counter_no,
                "counter_categories": status_to_update.counter_categories,
                "email": status_to_update.email

           

        }

        return jsonable_encoder(response)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You are not Super User"
    )

 
@count_router.get('/all/counter/')
async def get_all_counter( current_user: UserBase = Depends(get_current_user), db: Session = Depends(get_db)):

    
    print(current_user)
    user = current_user
    current_user = db.query(DbUser).filter(DbUser.username == user).first()

    if current_user.is_staff and current_user.is_active:
        all_counter = db.query(DbUser).options(load_only(*['id', 'email','username','counter_no','is_active','counter_categories','counter_name','is_staff'])).all()

        if all_counter is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"No Counter Availabe")

    
        return all_counter
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You are not SuperUser"
    )

 
@count_router.get('/counter/{counter_name}')
async def get_client_by_id(counter_name: str, current_user: UserBase = Depends(get_current_user), db: Session = Depends(get_db)):

    
    user = current_user

    current_user = db.query(DbUser).filter(DbUser.username == user).first()

    if current_user.is_staff and current_user.is_active:
        db_recepit = db.query(DbUser).filter(
            DbUser.counter_name == counter_name).first()

        if db_recepit is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Counter Name {counter_name} doestn't Exists")

        client = db.query(DbUser).filter(
            DbUser.counter_name == counter_name).first()
        response = {
                "id":client.id,
                "is_active":client.is_active,
                "username":client.username,
                "is_staff":client.is_staff,
                "counter_name":client.counter_name,
                "counter_no":client.counter_no,
                "counter_categories": client.counter_categories,
                "email": client.email


            }

        return jsonable_encoder(response)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You are not SuperUser"
    )

@count_router.patch('/counter-status/{counter_name}')
async def counter_status(counter_name: str, counter_status: CounterCategoriesModel, current_user: UserBase = Depends(get_current_user), db: Session = Depends(get_db)):

    print(current_user)
    username = current_user

    current_user = db.query(DbUser).filter(DbUser.username == username).first()

    if current_user.is_staff and current_user.is_active:
        db_counter_name = db.query(DbUser).filter(
            DbUser.counter_name == counter_name).first()

        if db_counter_name is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Counter name {counter_name} doestn't Exists")

        status_to_update = db.query(DbUser).filter(
            DbUser.counter_name == counter_name).first()

        status_to_update.counter_categories = counter_status.counter_categories
        

        db.commit()

        response = {
            "id":status_to_update.id,
                "is_active":status_to_update.is_active,
                "is_staff":status_to_update.is_staff,
                "username":status_to_update.username,
                "counter_name":status_to_update.counter_name,
                "counter_no":status_to_update.counter_no,
                "counter_categories": status_to_update.counter_categories,
                "email": status_to_update.email

           

        }

        return jsonable_encoder(response)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You are not Super User"
    )


# @router.get('/{id}')
# def get_articles(id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
#     return {'data': db_count.get_article(db, id),
#               'current_user': current_user}

    # read all article
# @router.get('/all',response_model=List[ArticleDisplay])
# def get_articles(db:Session=Depends(get_db)):
#     return db_article.get_article_s(db)

# read 5article or 10article
# @router.get('/specific-article',response_model=List[ArticleDisplay])
# def get_article_specific(page_num:int=1,page_size:int=5,db:Session=Depends(get_db)):
#     return db_count.get_specifi_article(db,page_num,page_size)


# # update

# @router.post('/{id}/update')
# def update_articles(id:int,request:ArticleBase,db:Session=Depends(get_db)):
#     return db_article.update_article(db,id,request)


# # delete

# @router.get('/delete/{id}',)
# def delete_articles(id,db:Session=Depends(get_db)):
#    return db_article.delete_article(id,db)
