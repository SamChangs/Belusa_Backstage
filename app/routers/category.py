
from Entity.meta import *
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Request
from tortoise.contrib.pydantic import pydantic_model_creator #從 Tortoise 模型創建 Pydantic 模型
from routers.users import get_oauth2_scheme

router = APIRouter(
    tags=["category"],
    dependencies=[Depends(get_oauth2_scheme)],
    responses={404: {"description": "Not found"}},
)

# ** product 模板
Category_Pydantic = pydantic_model_creator(Category, name='Category')
CategoryIn_Pydantic = pydantic_model_creator(Category, name='CategoryIn', exclude_readonly=True)
# print(User_Pydantic.schema()

@router.get('/category/me', response_model=List[Category_Pydantic])
async def get_category():
    category_obj = Category_Pydantic.from_queryset(Category.all())
    return await category_obj


async def all_category(category: Category_Pydantic = Depends(get_category)):

    return category

'''
@app.post('/category/me') 取得單一類別
'''
@router.get('/category/me/{id}', response_model=Category_Pydantic)
async def get_singl_category(id:int):
    category_single_obj = Category_Pydantic.from_queryset_single(Category.get(c_id=id))
    return await category_single_obj


'''
@app.post('/create/category') 新增類別
'''
@router.post('/create/category', response_model=Category_Pydantic)
async def create_category(category: CategoryIn_Pydantic):

    if not Category.category_name_alphanumeric(category.category_name):
        return False

    category_obj = Category(category_name = category.category_name)


    await category_obj.save()
    return await Category_Pydantic.from_tortoise_orm(category_obj)

'''
@router.post('/upload/category/{cid}') 修改類別
** c_id 要修改第幾筆類別資料
'''
@router.put("/update/category/{cid}", response_model=Category_Pydantic)
async def update_items(cid: int,categor: CategoryIn_Pydantic):
    await Product.filter(c_id=cid).update(**categor.dict(exclude_unset=True))
    return await Category_Pydantic.from_queryset_single(Category.get(c_id=cid))

async def get_update_category(cid:int):
    category_obj = await Category_Pydantic.from_queryset_single(Category.get(c_id=cid))
    return  category_obj

'''
@app.post('/delete/category') 刪除類別
** c_id 要修改第幾筆類別資料
'''
@router.delete("/delete/category/{cid}")
async def delete_category(cid: int):
    deleted_count = await Category.filter(c_id=cid).delete()
    if not deleted_count:
        raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail= f"Category {cid} not found"
                )
    return {"mes":f"Deleted Category {cid}"}
