import uvicorn
import json
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.hash import bcrypt
from tortoise.contrib.pydantic import pydantic_model_creator #從 Tortoise 模型創建 Pydantic 模型
from Entity.meta import *
from Model.OAuth2 import *
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token') #解析token是否符合OAuth2的規範
templates = Jinja2Templates(directory="templates")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

'''
新增 Pydantic 模板
** User 模板
'''
User_Pydantic = pydantic_model_creator(User, name='User') 
UserIn_Pydantic = pydantic_model_creator(User, name='UserIn', exclude_readonly=True)
UserOut_Pydantic = pydantic_model_creator(UserOut, name='UserOut')
# print(User_Pydantic.schema()
Auth = AuthUser(User_Pydantic,UserIn_Pydantic,UserOut_Pydantic)

# ** product 模板
Product_Pydantic = pydantic_model_creator(Product, name='Product') 
ProductIn_Pydantic = pydantic_model_creator(Product, name='ProductIn', exclude_readonly=True)
'''
web pages router
|------------------------------------------------------------------------------------|
'''
@app.get("/login", response_class=HTMLResponse)
async def read_login(request: Request):
    return templates.TemplateResponse("login.html",{"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html",{"request": request})

@app.get("/icons", response_class=HTMLResponse)
async def read_icons(request: Request):
    return templates.TemplateResponse("icons.html",{"request": request})

@app.get("/map", response_class=HTMLResponse)
async def read_map(request: Request):
    return templates.TemplateResponse("map.html",{"request": request})

@app.get("/create-tables", response_class=HTMLResponse)
async def read_create_tables(request: Request):
    return templates.TemplateResponse("formComponent/tablesform.html",{"request": request})

@app.get("/typography", response_class=HTMLResponse)
async def read_typography(request: Request):
    return templates.TemplateResponse("typography.html",{"request": request})

@app.get("/notifications", response_class=HTMLResponse)
async def read_notifications(request: Request):
    return templates.TemplateResponse("notifications.html",{"request": request})

@app.get("/user", response_class=HTMLResponse)
async def read_user(request: Request):
    return templates.TemplateResponse("user.html",{"request": request})

'''
|----------------------------------------------------------------------------------------------------|
@app.post('/token') 新增使用者token
'''
@app.post('/token')
async def Auth_generate_rertoken( form_data:OAuth2PasswordRequestForm = Depends()):
    res = await Auth.generate_token(form_data)
    print(form_data)
    # return res

'''
@app.post('/users') 註冊使用者
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
    currentuser = Auth.get_current_user(token)
    return await currentuser    

'''
@app.get('/users/me) 取得使用者
** get_oauth2_scheme 執行 get_user 前先去執行 get_oauth2_scheme
'''
@app.get('/users/me', response_model=UserOut_Pydantic)
async def get_user(user: User_Pydantic = Depends(get_oauth2_scheme)):
    return user    

'''
@app.post('/product/me') 取得所有產品
@app.get("/tables", response_class=HTMLResponse) 傳遞產品參數並呈現在tables.html
** product_obj : 產品字典物件
'''
@app.get('/product/me', response_model=List[Product_Pydantic])
async def get_product():
    product_obj = Product_Pydantic.from_queryset(Product.all()) 
    return await product_obj

@app.get("/tables", response_class=HTMLResponse)
async def read_tables(request: Request, product: Product_Pydantic = Depends(get_product)):
    return templates.TemplateResponse("tables.html",{"request": request, "productpric": product})

'''
@app.post('/product/me') 取得單一產品
'''
@app.get('/product/me/{id}', response_model=Product_Pydantic)
async def get_singl_product(id:int):
    product_single_obj = Product_Pydantic.from_queryset_single(Product.get(p_id=id))
    return await product_single_obj


'''
@app.post('/create/product') 新增產品
** get_oauth2_scheme 執行 get_user 前先去執行 get_oauth2_scheme
'''
@app.post('/create/product', response_model=Product_Pydantic)
async def create_product(product: ProductIn_Pydantic):
    
    if not Product.product_name_alphanumeric(product.product_name):
        return False
    if not Product.price_alphanumeric(product.price):
        return False
    if not Product.category_alphanumeric(product.category):
        return False
    
    product_obj = Product(product_name = product.product_name, price=product.price,
                  image=product.image, category=product.category, is_hot=product.is_hot)
    

    await product_obj.save()
    return await Product_Pydantic.from_tortoise_orm(product_obj)

'''
@app.post('/upload/item/{pid}') 修改產品
** p_id 要修改第幾筆產品資料
'''
@app.put("/update/item/{pid}", response_model=Product_Pydantic)
async def update_product(pid: int,product: ProductIn_Pydantic):
    await Product.filter(p_id=pid).update(**product.dict(exclude_unset=True))
    return await Product_Pydantic.from_queryset_single(Product.get(p_id=pid))

@app.get("/update/item/{pid}", response_class=HTMLResponse)
async def read_single_tables(request: Request,pid:int):
    product_obj = await Product_Pydantic.from_queryset_single(Product.get(p_id=pid))
    return  templates.TemplateResponse("formComponent/tablesformUpdate.html",{"request": request, "productpric": product_obj, "p_id": pid})

'''
@app.post('/delete/item') 刪除產品
** p_id 要修改第幾筆產品資料
'''
@app.delete("/delete/item/{pid}")
async def delete_product(pid: int):
    deleted_count = await Product.filter(p_id=pid).delete()
    if not deleted_count:
        raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail= f"Product {pid} not found"
                )
    return {"mes":f"Deleted Product {pid}"}

register_tortoise(
    app, 
    db_url= DATABASE_URL,
    modules={'models': ['main']},#models對應的檔案名稱
    generate_schemas=True, #如果數據庫爲空，則自動生成對應表單,生產環境不要開
    add_exception_handlers=True #生產環境不要開，會泄露調試信息
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")
