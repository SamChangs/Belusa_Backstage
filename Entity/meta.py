import os
import databases
from fastapi import FastAPI
from dotenv import load_dotenv
from tortoise.models import Model 
from tortoise import fields 
from passlib.hash import bcrypt
from pydantic import validator
from tortoise.contrib.fastapi import register_tortoise

load_dotenv() #載入.env 使 getenv 可以讀取到

DATABASE_URL = os.getenv('PostgreSQL',default=None)
database = databases.Database(DATABASE_URL)
app = FastAPI()

'''
繼承Model使class可變為資料表
'''
class User(Model): 
    id = fields.IntField(pk=True) #主鍵必不可少
    storename = fields.CharField(20, null=False)
    account = fields.CharField(50, unique=True)
    password_hash = fields.CharField(128,null=False)
    
    def verify_password(self, password):
        print(self.password_hash)
        return bcrypt.verify(password, self.password_hash)
        
    @validator('password')
    def password_rules(cls, v):
        if len(v) < 4:
            raise ValueError('password too short')
        assert v != '', 'Empty strings are not allowed.'
        return v

    @validator('account')
    def account_alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        assert v != '', 'Empty strings are not allowed.'
        return v

'''
輸出使用者資料，不包含密碼
'''
class UserOut(Model): 
    id = fields.IntField(pk=True) #主鍵必不可少
    storename = fields.CharField(20, null=False)
    account = fields.CharField(50, unique=True)


class Order(Model): 
    o_id = fields.IntField(pk=True) #主鍵必不可少
    oder_name = fields.CharField(20, null=False)
    price = fields.IntField (max_value=5,unique=True)
    number = fields.CharField(128,null=False)
    add_time = fields.DatetimeField()


class Product(Model): 
    p_id = fields.IntField(pk=True) #主鍵必不可少
    product_name = fields.CharField(20, null=False,unique=True)
    price = fields.IntField(max_value=5,null=False)
    image = fields.TextField()
    category  = fields.CharField(20, null=False)
    is_hot =  fields.BooleanField()
    add_time = fields.DatetimeField(auto_now_add=True)

    @validator('product_name')
    def product_name_alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        assert v != '', 'Empty strings are not allowed.'
        return v

    @validator('price')
    def price_alphanumeric(cls, v):
        assert v != '', 'Empty strings are not allowed.'
        return v

    @validator('category')
    def category_alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        assert v != '', 'Empty strings are not allowed.'
        return v
    
class Category(Model): 
    c_id = fields.IntField(pk=True) #主鍵必不可少
    category_name = fields.CharField(20, null=False)
    add_time = fields.DatetimeField(auto_now_add=True)
   