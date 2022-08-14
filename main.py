from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}










































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