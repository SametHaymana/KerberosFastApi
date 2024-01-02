from fastapi import APIRouter, HTTPException,Request
import datetime as dt
import bcrypt
import jwt

from src.models import User, Servers
from src.schemas import *


router = APIRouter()

serverId = 1

# Get User Own account
@router.get("/myAccount")
async def get_myAccount(request: Request):
    # Get Server infos from db
    server = await Servers.get_or_none(id=serverId)
    
    if server is None:
        return HTTPException(status_code=404, detail="Server not found")
    
    
    # Read the token from the header
    # Check if token is valid
    # Return user account
    token = request.headers["Authorization"].split(" ")[1]
    
    # Decode token
    # Check if token is valid
    # Return user account
    try:
        payload = jwt.decode(token, server.secret, algorithms=["HS256"])
    except:
        return HTTPException(status_code=401, detail="Invalid token")
    
    # Get userId from token named sub
    userId = payload["sub"]
    
    # Get user from db
    user = await User.get_or_none(id=userId)
    
    if user is None:
        return HTTPException(status_code=404, detail="User not found")
    
    
    return GET_ACCOUNT_RESPONSE(username=user.username)




@router.patch("/updatePassword")
async def update_password(request:Request ,param: UPDATE_PASSWORD_REQUEST):
    # Get Server infos from db
    server = await Servers.get_or_none(id=serverId)
    
    if server is None:
        return HTTPException(status_code=404, detail="Server not found")
    
    
    # Read the token from the header
    # Check if token is valid
    # Return user account
    token = request.headers["Authorization"].split(" ")[1]
    
    # Decode token
    # Check if token is valid
    # Return user account
    try:
        payload = jwt.decode(token, server.secret, algorithms=["HS256"])
    except:
        return HTTPException(status_code=401, detail="Invalid token")
    
    # Get userId from token named sub
    userId = payload["sub"]
    
    # Get user from db
    user = await User.get_or_none(id=userId)
    
    if user is None:
        return HTTPException(status_code=404, detail="User not found")
    
    
    # hash new password
    hashedPassword = bcrypt.hashpw(param.newPassword.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Update user password
    user.password = hashedPassword
    
    await user.save()
    
    return UPDATE_PASSWORD_RESPONSE(success=True)

# Creating User functions
@router.post("/createUser")
async def create_user(request:Request, param: CREATE_USER_REQUEST):
    # Get Server infos from db
    server = await Servers.get_or_none(id=serverId)
    
    if server is None:
        return HTTPException(status_code=404, detail="Server not found")
    
    
    # Read the token from the header
    # Check if token is valid
    # Return user account
    token = request.headers["Authorization"].split(" ")[1]
    
    # Decode token
    # Check if token is valid
    # Return user account
    try:
        payload = jwt.decode(token, server.secret, algorithms=["HS256"])
    except:
        return HTTPException(status_code=401, detail="Invalid token")
    
    # Get userId from token named sub
    userId = payload["sub"]
    
    # Get user from db
    user = await User.get_or_none(id=userId)
    
    if user is None:
        return HTTPException(status_code=404, detail="User not found")
    
    # Admin User just can create user
    if user.isAdministrator == False:
        return HTTPException(status_code=401, detail="You are not authorized to create user")
    
    # Create user
    # hash password
    hashedPassword = bcrypt.hashpw(param.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    await User.create(username=param.username, password=hashedPassword)
    
    return CREATE_USER_RESPONSE(username=param.username)

