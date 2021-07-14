from fastapi import APIRouter, Request,Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from routers.items import all_items,get_update_items
from typing import List
from dependencies import auth_pages


router = APIRouter(
    tags=["pages"],
    responses={404: {"description": "Not found"}}
    )

templates = Jinja2Templates(directory="../templates")

'''
web pages router
|------------------------------------------------------------------------------------|
'''

@router.get("/login",  response_class=HTMLResponse)
async def read_login(request: Request):

    return templates.TemplateResponse("login.html",{"request": request})

@router.get("/dashboard", response_class=HTMLResponse)
async def read_dashboard(request: Request,token: str = Depends(auth_pages)):

    if token != False:
        return templates.TemplateResponse("dashboard.html",{"request": request})
    else:
        return RedirectResponse("/login")

@router.get("/tables/",response_class=HTMLResponse)
async def read_table(request: Request, product: List = Depends(all_items),token: str = Depends(auth_pages)):

    if token != False:
        return templates.TemplateResponse("tables.html",{"request": request, "productpric": product})
    else:
        return RedirectResponse("/login")

@router.get("/category",response_class=HTMLResponse)
async def read_category(request: Request,token: str = Depends(auth_pages)):

    if token != False:
        return templates.TemplateResponse("category.html",{"request": request})
    else:
        return RedirectResponse("/login")

@router.get("/order", response_class=HTMLResponse)
async def read_order(request: Request,token: str = Depends(auth_pages)):

    if token != False:
        return templates.TemplateResponse("order.html",{"request": request})
    else:
        return RedirectResponse("/login")

@router.get("/map", response_class=HTMLResponse)
async def read_map(request: Request,token: str = Depends(auth_pages)):

    if token != False:
        return templates.TemplateResponse("map.html",{"request": request})
    else:
        return RedirectResponse("/login")

@router.get("/user", response_class=HTMLResponse)
async def read_user(request: Request,token: str = Depends(auth_pages)):

    if token != False:
        return templates.TemplateResponse("user.html",{"request": request})
    else:
        return RedirectResponse("/login")

@router.get("/typography", response_class=HTMLResponse)
async def read_typography(request: Request,token: str = Depends(auth_pages)):
    if token != False:
        return templates.TemplateResponse("typography.html",{"request": request})
    else:
        return RedirectResponse("/login")

@router.get("/create-tables", response_class=HTMLResponse)
async def read_create_tables(request: Request,token: str = Depends(auth_pages)):

    if token != False:
        return templates.TemplateResponse("formComponent/tablesform.html",{"request": request})
    else:
        return RedirectResponse("/login")

@router.get("/update/item/{pid}", response_class=HTMLResponse)
async def read_single_items(request: Request, pid:int,token: str = Depends(auth_pages)):

    if token != False:
        product = get_update_items(pid)
        return  templates.TemplateResponse("formComponent/tablesformUpdate.html",{"request": request, "productpric": product, "p_id": pid})
    else:
        return RedirectResponse("/login")

@router.get("/create-category", response_class=HTMLResponse)
async def read_create_tables(request: Request,token: str = Depends(auth_pages)):

    if token != False:
        return templates.TemplateResponse("formComponent/tablesform.html",{"request": request})
    else:
        return RedirectResponse("/login")

@router.get("/update/category/{cid}", response_class=HTMLResponse)
async def read_single_items(request: Request, pid:int,token: str = Depends(auth_pages)):

    if token != False:
        product = get_update_items(pid)
        return  templates.TemplateResponse("formComponent/tablesformUpdate.html",{"request": request, "productpric": product, "p_id": pid})
    else:
        return RedirectResponse("/login")
