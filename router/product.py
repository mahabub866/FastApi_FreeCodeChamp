# from enum import Enum
# import time 
# from fastapi import APIRouter, status, Response,Form, Query, Body, Path, Depends, Header, Cookie
# from typing import Dict, List, Optional, Union
# from fastapi.responses import HTMLResponse, PlainTextResponse

# from sqlalchemy.orm.session import Session
# from custom_log import log
# from db.database import get_db
# from db import db_count
# from schemas import ArticleBase, ArticleDisplay

# router = APIRouter(
#     prefix='/prodduct',
#     tags=['Product']

# )
# products = ['watch', 'camera', 'phone']
# async def time_consuming_functionality():
#     time.sleep(5)
#     return 'ok'
# @router.post('/new')
# def create_product(name:str=Form(...)):
#     products.append(name)
#     return products

# @router.get('/withheader')
# def get_products(response: Response,
#                  custom_header: Optional[List[str]] = Header(None),
#                  text_cookie: Optional[str] = Cookie(None)):
#     log("MyAPI","Call to get all products")             
#     if custom_header:
#         response.headers['custome_response_header'] = " and ".join(custom_header)
#         return {'data': products,
#             'custom_header': custom_header,
#             'my_cookie': text_cookie}


# @router.get('/all')
# async def get_all_product():
#     await time_consuming_functionality()
#     data = " ".join(products)
#     respone = Response(content=data, media_type='text/plain')
#     respone.set_cookie(key='test_cookie', value="cookie value test")
#     return respone


# @router.get('/{id}', responses={200: {
#     "content": {
#         "text/html": {
#             "Example": "<div>Product<div>"
#         }
#     },
#     "description": "Return the html for an object"
# },
#     404: {
#     "content": {
#         "text/plain": {
#             "Example": "Product not Availabe"
#         }
#     },
#     "description": "A ClearText error Message"

# }
# })
# def get_product(id: int):
#     if id > len(products):
#         out = "please Not availabe "
#         return PlainTextResponse(status_code=404, content=out, media_type='text/plain')
#     else:
#         product = products[id]
#         out = f'''
#         <head>
#             <style>
#             .product{{
#                 width:500px;
#                 height:30px;
#                 border:2px inset green;
#                 background-color:lightblue;
#                 text-align:center;

#             }}

#             </style>
#             </head>
#             <div class="product">{product}</div>
#         '''

#     return HTMLResponse(content=out, media_type='text/plain')
