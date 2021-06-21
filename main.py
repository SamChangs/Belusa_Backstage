import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.hash import bcrypt
from starlette import responses
from tortoise.contrib.pydantic import pydantic_model_creator #從 Tortoise 模型創建 Pydantic 模型
from Entity.meta import *
from tortoise.contrib.fastapi import register_tortoise
from Model.OAuth2 import *
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI()

User_Pydantic = pydantic_model_creator(User, name='User') 
# print(User_Pydantic.schema()
UserIn_Pydantic = pydantic_model_creator(User, name='UserIn', exclude_readonly=True)
UserOut_Pydantic = pydantic_model_creator(UserOut, name='UserOut')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token') #解析token是否符合OAuth2的規範
templates = Jinja2Templates(directory="templates")
Auth = AuthUser(User_Pydantic,UserIn_Pydantic,UserOut_Pydantic)

app.mount("/assets", StaticFiles(directory="assets"), name="assets")

'''
web pages
'''
@app.get("/login", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("login.html",{"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("dashboard.html",{"request": request})

@app.get("/icons", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("icons.html",{"request": request})

@app.get("/map", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("map.html",{"request": request})

@app.get("/tables", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("tables.html",{"request": request})

@app.get("/create-tables", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("formComponent/tablesform.html",{"request": request})

@app.get("/typography", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("typography.html",{"request": request})

@app.get("/notifications", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("notifications.html",{"request": request})

@app.get("/user", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("user.html",{"request": request})


@app.post('/token')
async def Auth_generate_rertoken( form_data:OAuth2PasswordRequestForm = Depends()):
    res = await Auth.generate_token(form_data)
    print(form_data)
    # return res

'''
response_model 根據定義的模組回傳相對應的型別，例如User_Pydantic的型別有以下:
id : int
Storename :str
account :str
password_hash :str

|-----------------------------------------------------|

User_Pydantic.from_tortoise_orm() 連線到table，可以根據參數查詢資料 
例如有一個變數 user = User.get(id="1")
則 User_Pydantic.from_tortoise_orm(user) 會連結 id 為 1 的使用者資料
'''
@app.post('/users', response_model=User_Pydantic) 
async def create_user(user: UserIn_Pydantic, accesskey: str):
    
    if not User.account_alphanumeric(user.account):
        return False
    if not User.password_rules(user.password_hash):
        return False
    if accesskey != "wtleelab":
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED, 
            detail='驗證碼錯誤'
        )
    
    user_obj = User(storename = user.storename, account=user.account, password_hash=bcrypt.hash(user.password_hash))

    await user_obj.save()
    return await User_Pydantic.from_tortoise_orm(user_obj)

'''
Depends : 類似裝飾器的概念，從函數中獲取結果(不一定要是函式)。
將該結果分配給路徑操作函數中的參數。
'''
async def get_oauth2_scheme(token: str = Depends(oauth2_scheme)):
    aa = Auth.get_current_user(token)
    return await aa    

@app.get('/users/me', response_model=UserOut_Pydantic)
async def get_user(user: User_Pydantic = Depends(get_oauth2_scheme)):
    return user    


register_tortoise(
    app, 
    db_url= DATABASE_URL,
    modules={'models': ['main']},#models對應的檔案名稱
    generate_schemas=True, #如果數據庫爲空，則自動生成對應表單,生產環境不要開
    add_exception_handlers=True #生產環境不要開，會泄露調試信息
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")
