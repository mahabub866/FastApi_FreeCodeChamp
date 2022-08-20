from enum import Enum
import time
from tracemalloc import start

from typing import Optional, Union


from fastapi.responses import JSONResponse,PlainTextResponse
from fastapi.exceptions import HTTPException
from fastapi import FastAPI, Query, Path,status,Response,Request
from pydantic import BaseModel
from exceptions import StoryException
from router import blog_get,blog_post,user,article,product,file
from auth import authentication
from db.database import engine
from db import models
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
app = FastAPI()


app.include_router(blog_get.router)
app.include_router(blog_post.router)
app.include_router(user.router)
app.include_router(article.router)
app.include_router(product.router)
app.include_router(authentication.router)
app.include_router(file.router)




@app.exception_handler(StoryException)
def story_exception_handler(request:Request,exc:StoryException):
    return JSONResponse(status_code=418,content={'detail':exc.name})


# @app.exception_handler(HTTPException)
# def custom_handler(request:Request,exc:HTTPException):
#     return PlainTextResponse(str(exc),status_code=400,)

models.Base.metadata.create_all(engine)

@app.middleware("http")
async def add_middleware(request:Request,call_next):
    start_time=time.time()
    response= await call_next(request)
    duration=time.time()-start_time
    response.headers['duration']=str(duration)
    return response

origins=[
    'http://localhost:4350'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount('/files',StaticFiles(directory="files"),name='files')

# class Item(BaseModel):
#     name: str
#     price: float
#     is_offer: Union[bool, None] = None


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int = Path(title="The ID of the item to get", ge=1, le=7), q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}



# from fastapi import FastAPI,Path


# app=FastAPI()

# students={
#     1:{
#         "name":"Mahabub",
#         "age":17,
#         "class":"Inter 2nd Year"
#     },
#     2:{
#         "name":"Mak",
#         "age":9,
#         "class":"Inter 1nd Year"
#     },
#     3:{
#         "name":"shamol",
#         "age":22,
#         "class":"Inter Year"
#     },
#     4:{
#         "name":"Rahman",
#         "age":22,
#         "class":"Inter 3rd Year"
#     }
# }

# @app.get('/')
# def get():
#     return {"hello":"world"}

# @app.get('/get-student/{student_id}')
# def get_students(students_id:int=Path(None,description="The id of the student you want to view",gt=0,lt=7)):
#     return students[students_id]
