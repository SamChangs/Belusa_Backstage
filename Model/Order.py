from tortoise.contrib.pydantic import pydantic_model_creator #從 Tortoise 模型創建 Pydantic 模型



Oder_Pydantic = pydantic_model_creator(User, name='User') 
# print(User_Pydantic.schema()
OderIn_Pydantic = pydantic_model_creator(User, name='UserIn', exclude_readonly=True)

@app.post('/oder', response_model=Oder_Pydantic) 
async def create_oder(user: OderIn_Pydantic):
    
    if not User.account_alphanumeric(user.account):
        return False
    if not User.password_rules(user.password_hash):
        return False
   
    user_obj = oder(storename = user.storename, account=user.account, password_hash=bcrypt.hash(user.password_hash))

    await user_obj.save()
    return await Oder_Pydantic.from_tortoise_orm(user_obj)