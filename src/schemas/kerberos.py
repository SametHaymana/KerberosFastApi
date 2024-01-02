from pydantic import BaseModel

class AS_REQUEST(BaseModel):
    username: str
    password: str
    serverId: int
    
class AS_RESPONSE(BaseModel):
    serverId: int
    tgt: str

class TGS_REQUEST(BaseModel):
    serverId: int
    tgt: str

    
class TGS_RESPONSE(BaseModel):
    serverId: int
    ticket: str

class AP_REQUEST(BaseModel):
    ticket: str
    serverId: int
    sessionKey: str

