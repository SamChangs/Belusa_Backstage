import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Request, Response, Cookie
from fastapi.responses import RedirectResponse
from routers import items, users, webtemplates
from Entity.meta import *
from Model.OAuth2 import *
from fastapi.responses import HTMLResponse

app = FastAPI()

'''
aporoute
'''
app.include_router(users.router)
app.include_router(items.router)
app.include_router(webtemplates.router)
            
@app.get("/auth/logout", response_class=HTMLResponse)
def logout():
   response = RedirectResponse(url="/login")
   response.delete_cookie("access_token")
   return response


register_tortoise(
    app, 
    db_url= DATABASE_URL,
    modules={'models': ['main']},#models對應的檔案名稱
    generate_schemas=True, #如果數據庫爲空，則自動生成對應表單,生產環境不要開
    add_exception_handlers=True #生產環境不要開，會泄露調試信息
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")


