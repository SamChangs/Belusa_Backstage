from fastapi import APIRouter, Response, Depends, Cookie, HTTPException, status
from tortoise.contrib.pydantic import pydantic_model_creator #從 Tortoise 模型創建 Pydantic 模型
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from Entity.meta import *
from Model.OAuth2 import *

router = APIRouter()

'''
新增 Pydantic 模板
** User 模板
'''
User_Pydantic = pydantic_model_creator(User, name='User') 
UserIn_Pydantic = pydantic_model_creator(User, name='UserIn', exclude_readonly=True)

# print(User_Pydantic.schema()
Auth = AuthUser(User_Pydantic,UserIn_Pydantic)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token') #解析token是否符合OAuth2的規範


'''
|----------------------------------------------------------------------------------------------------|
@app.post('/login_user') 比對使用者帳密，回傳access_token
'''
@router.post('/login_user',tags=["users"])
async def Auth_generate_rertoken(response: Response,form_data:OAuth2PasswordRequestForm = Depends()):
    res = await Auth.generate_token(form_data)
    response.set_cookie(key="access_token", value= str(res))

    return res

'''
Depends : 類似裝飾器的概念，從函數中獲取結果(不一定要是函式)。
將該結果分配給路徑操作函數中的參數。

oauth2_scheme : 是access_token
'''
async def get_oauth2_scheme(token: str = Depends(oauth2_scheme)):
    currentuser = Auth.get_current_user(token)

    return await currentuser    

'''
@app.get('/users/me) 取得使用者
** get_oauth2_scheme 執行 get_user 前先去執行 get_oauth2_scheme
'''
@router.get('/users/me',tags=["users"], response_model=UserOut)
async def get_user(user: User_Pydantic = Depends(get_oauth2_scheme)):
    return user    

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
@router.post('/users', tags=["users"], response_model=User_Pydantic) 
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

