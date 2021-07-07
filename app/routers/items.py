
from Entity.meta import *
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from tortoise.contrib.pydantic import pydantic_model_creator #從 Tortoise 模型創建 Pydantic 模型


router = APIRouter(
    tags=["items"],
    responses={404: {"description": "Not found"}},
)

# ** product 模板
Product_Pydantic = pydantic_model_creator(Product, name='Product') 
ProductIn_Pydantic = pydantic_model_creator(Product, name='ProductIn', exclude_readonly=True)


@router.get('/product/me', response_model=List[Product_Pydantic])
async def get_items():
    product_obj = Product_Pydantic.from_queryset(Product.all()) 
    return await product_obj


async def all_items(product: Product_Pydantic = Depends(get_items)):
    
    return product

'''
@app.post('/product/me') 取得單一產品
'''
@router.get('/product/me/{id}', response_model=Product_Pydantic)
async def get_singl_items(id:int):
    product_single_obj = Product_Pydantic.from_queryset_single(Product.get(p_id=id))
    return await product_single_obj


'''
@app.post('/create/product') 新增產品
** get_oauth2_scheme 執行 get_user 前先去執行 get_oauth2_scheme
'''
@router.post('/create/product', response_model=Product_Pydantic)
async def create_items(product: ProductIn_Pydantic):
    
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
@router.post('/upload/item/{pid}') 修改產品
** p_id 要修改第幾筆產品資料
'''
@router.put("/update/item/{pid}", response_model=Product_Pydantic)
async def update_items(pid: int,product: ProductIn_Pydantic):
    await Product.filter(p_id=pid).update(**product.dict(exclude_unset=True))
    return await Product_Pydantic.from_queryset_single(Product.get(p_id=pid))

async def get_update_items(pid:int):
    product_obj = await Product_Pydantic.from_queryset_single(Product.get(p_id=pid))
    return  product_obj

'''
@app.post('/delete/item') 刪除產品
** p_id 要修改第幾筆產品資料
'''
@router.delete("/delete/item/{pid}")
async def delete_items(pid: int):
    deleted_count = await Product.filter(p_id=pid).delete()
    if not deleted_count:
        raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail= f"Product {pid} not found"
                )
    return {"mes":f"Deleted Product {pid}"}
