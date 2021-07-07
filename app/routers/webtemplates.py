from fastapi import APIRouter, Request,Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from routers.items import all_items,get_update_items
from typing import List
from dependencies import read_tables

router = APIRouter(
    tags=["pages"],
    responses={404: {"description": "Not found"}}
    )

router.mount("/assets", StaticFiles(directory="../assets"), name="assets")
templates = Jinja2Templates(directory="../templates")

'''
web pages router
|------------------------------------------------------------------------------------|
'''

@router.get("/login",  response_class=HTMLResponse)
async def read_login(request: Request):
    
    return templates.TemplateResponse("login.html",{"request": request})

@router.get("/user", dependencies=[Depends(read_tables)], response_class=HTMLResponse)
async def read_user(request: Request):
    return templates.TemplateResponse("user.html",{"request": request})

@router.get("/dashboard",dependencies=[Depends(read_tables)], response_class=HTMLResponse)
async def read_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html",{"request": request})

@router.get("/icons", dependencies=[Depends(read_tables)],response_class=HTMLResponse)
async def read_icons(request: Request):
    return templates.TemplateResponse("icons.html",{"request": request})

@router.get("/map", dependencies=[Depends(read_tables)], response_class=HTMLResponse)
async def read_map(request: Request):
    return templates.TemplateResponse("map.html",{"request": request})

@router.get("/create-tables", dependencies=[Depends(read_tables)], response_class=HTMLResponse)
async def read_create_tables(request: Request):
    return templates.TemplateResponse("formComponent/tablesform.html",{"request": request})

@router.get("/typography", dependencies=[Depends(read_tables)], response_class=HTMLResponse)
async def read_typography(request: Request):
    return templates.TemplateResponse("typography.html",{"request": request})

@router.get("/notifications", dependencies=[Depends(read_tables)], response_class=HTMLResponse)
async def read_notifications(request: Request):
    return templates.TemplateResponse("notifications.html",{"request": request})

@router.get("/tables/",dependencies=[Depends(read_tables)], response_class=HTMLResponse)
async def read_tables(request: Request, product: List = Depends(all_items)):
 
    return templates.TemplateResponse("tables.html",{"request": request, "productpric": product})

@router.get("/update/item/{pid}",dependencies=[Depends(read_tables)],  response_class=HTMLResponse)
async def read_single_items(request: Request, pid:int):
    product = get_update_items(pid)
    return  templates.TemplateResponse("formComponent/tablesformUpdate.html",{"request": request, "productpric": product, "p_id": pid})


