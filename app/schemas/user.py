from pydantic import BaseModel,ConfigDict

class UserCreate(BaseModel):
    email:str
    password:str
    
class UserLogin(BaseModel):
    email:str
    password:str

class UserResponse(BaseModel):
    id:int
    email:str
    role:str
    is_active:bool
    model_config=ConfigDict(from_attributes=True)

class RefreshTokenRequest(BaseModel):
    refresh_token: str