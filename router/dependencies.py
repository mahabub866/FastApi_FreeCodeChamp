
from fastapi.param_functions import Depends
from fastapi import APIRouter,Request

router=APIRouter(prefix='/dependencies',tags=['Dependencies'])

def convert_params(request:Request,seperator:str):
    query=[]
    for key,value in request.query_params.items():
        query.append(f"{key}{seperator}{value}")
    return query


def conver_headers(request:Request,separator:str='--',query=Depends(convert_params)):
    out_headers=[]
    for key,value in request.headers.items():
        out_headers.append(f"{key}{separator}{value}")
    return {
        'headers':out_headers,
        'querys':query,
    }

@router.get('')
def get_items(separator:str='--',headers=Depends(conver_headers)):
    return {
        'items':['a','b','c'],
        'headers':headers
    }

@router.post('/new')
def create_item(separator:str='--',headers=Depends(conver_headers)):
    return{
        'result':'new item created',
        'headers':headers
    }

class Account:
    def __init__(self,name:str,email:str):
        self.name=name
        self.email=email

@router.post('/user')
def create_user(name:str,email:str,password:str,account:Account=Depends(Account)):
    return {
        'name':account.name,
        'email':account.email
    }