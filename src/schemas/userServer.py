from pydantic import BaseModel

class GET_ACCOUNT_RESPONSE(BaseModel):
    username: str

class UPDATE_PASSWORD_REQUEST(BaseModel):
    newPassword: str

class UPDATE_PASSWORD_RESPONSE(BaseModel):
    success: bool

class CREATE_USER_REQUEST(BaseModel):
    username: str
    password: str
    
class CREATE_USER_RESPONSE(BaseModel):
    username: str
    
class UPDATE_SERVER_SECRET_REQUEST(BaseModel):
    serverId: int
    newSecret: str

class UPDATE_SERVER_SECRET_RESPONSE(BaseModel):
    success: bool