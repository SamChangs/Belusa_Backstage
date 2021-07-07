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

@router.get("/login", tags= None ,response_class=HTMLResponse)
async def read_login(request: Request):
    return templates.TemplateResponse("login.html",{"request": request})

@router.get("/user", response_class=HTMLResponse)
async def read_user(request: Request):
    return templates.TemplateResponse("user.html",{"request": request})

@router.get("/dashboard", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html",{"request": request})

@router.get("/icons", response_class=HTMLResponse)
async def read_icons(request: Request):
    return templates.TemplateResponse("icons.html",{"request": request})

@router.get("/map", response_class=HTMLResponse)
async def read_map(request: Request):
    return templates.TemplateResponse("map.html",{"request": request})

@router.get("/create-tables", response_class=HTMLResponse)
async def read_create_tables(request: Request):
    return templates.TemplateResponse("formComponent/tablesform.html",{"request": request})

@router.get("/typography", response_class=HTMLResponse)
async def read_typography(request: Request):
    return templates.TemplateResponse("typography.html",{"request": request})

@router.get("/notifications", response_class=HTMLResponse)
async def read_notifications(request: Request):
    return templates.TemplateResponse("notifications.html",{"request": request})

@router.get("/tables/", response_class=HTMLResponse)
async def read_tables(request: Request, product: List = Depends(all_items)):
 
    return templates.TemplateResponse("tables.html",{"request": request, "productpric": product})

@router.get("/update/item/{pid}", response_class=HTMLResponse)
async def read_single_items(request: Request, pid:int):
    product = get_update_items(pid)
    return  templates.TemplateResponse("formComponent/tablesformUpdate.html",{"request": request, "productpric": product, "p_id": pid})


# import uvicorn
# from fastapi import FastAPI, Depends, HTTPException, status, Request, Response, Cookie
# from fastapi.responses import RedirectResponse
# from routers import items, users, webtemplates
# from Entity.meta import *
# from Model.OAuth2 import *
# from fastapi.responses import HTMLResponse
# from dependencies import read_tables

# app = FastAPI()

# '''
# apiRoute
# '''
# app.include_router(users.router)
# app.include_router(items.router)
# app.include_router(webtemplates.router,
#                    dependencies=[Depends(read_tables)],
#                    responses={403: {"description": "please login page"}}
#                    )


# @ app.get("/auth/logout", response_class=HTMLResponse)
# def logout():
#    response = RedirectResponse(url="/login")
#    response.delete_cookie("access_token")
#    return response


# register_tortoise(
#     app, 
#     db_url= DATABASE_URL,
#     modules={'models': ['main']},#models對應的檔案名稱
#     generate_schemas=True, #如果數據庫爲空，則自動生成對應表單,生產環境不要開
#     add_exception_handlers=True #生產環境不要開，會泄露調試信息
# )

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")



