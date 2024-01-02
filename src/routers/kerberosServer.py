from fastapi import APIRouter, HTTPException,Request
import datetime as dt
import time
import bcrypt
import jwt
import os

from src.schemas import *
from src.models.users import User
from src.models.servers import Servers 

router = APIRouter()


kerberosSecret = os.getenv("SECRET_KEY") if os.getenv("SECRET_KEY") else "secret" 


@router.post("/getTGT")
async def login(request: AS_REQUEST):
    # Find user in database
    _user = await User.get_or_none(username=request.username)
    
    # Check if user exists
    if _user is None:
        return HTTPException(status_code=404, detail="User not found")
    
    # Check if password is correct
    # hash current password
    # compare with stored password

    isValidPassword = bcrypt.checkpw(request.password.encode('utf-8'), _user.password.encode('utf-8'))
    
    if not isValidPassword:
        return HTTPException(status_code=404, detail="Incorrect password")
    
    
    _server = await Servers.get_or_none(id=request.serverId)
    if _server is None:
        return HTTPException(status_code=404, detail="Server not found")
    
    
    
    # Generate TGT (Ticket Granting Ticket)
    tgt_payload = {
        "sub": _user.id,
        "server_id": _server.id,
        # İsued At Time
        "iat": dt.datetime.utcnow(),
        # Expiration Time
        "exp": dt.datetime.utcnow() + dt.timedelta(minutes=5),
    }
    tgt = jwt.encode(tgt_payload, kerberosSecret, algorithm="HS256")

    response = AS_RESPONSE(serverId=request.serverId, tgt=tgt)

    return response


@router.post("/getTGS")
async def getTGS(request: TGS_REQUEST):
    
    # Decode TGT
    try:
        tgt_payload = jwt.decode(request.tgt, kerberosSecret, algorithms=["HS256"])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid TGT")
    
   
    # Check if TGT is expired
    if tgt_payload["exp"] < time.time():
        raise HTTPException(status_code=401, detail="Expired TGT")
    
    
    # Check TGS is for the requested server
    if tgt_payload["server_id"] != request.serverId:
        raise HTTPException(status_code=401, detail="Invalid TGS")
    
    # Find server in database
    _server = await Servers.get_or_none(id=request.serverId)
    
    # Check if server exists
    if _server is None:
        return HTTPException(status_code=404, detail="Server not found")
    
    # Generate Ticket for requested server
    ticket_payload = {
        "sub": tgt_payload["sub"],
        "server_id": request.serverId,
        # İsued At Time
        "iat": dt.datetime.utcnow(),
        # Expiration Time
        "exp": dt.datetime.utcnow() + dt.timedelta(minutes=150),
    }
    
    # This time we will use the server secret to sign the ticket
    ticket = jwt.encode(ticket_payload, _server.secret, algorithm="HS256")
    
    
    response = TGS_RESPONSE(serverId=request.serverId, ticket=ticket)
    return response    





# Update User Server Secret Restiricted for Admin
@router.post("/updateServerSecret")
async def update_server_secret(request:Request,param: UPDATE_SERVER_SECRET_REQUEST):
    # Get Server infos from db
    server = await Servers.get_or_none(id=param.serverId)
    
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
    
    
    # Update server secret
    server.secret = param.newSecret
    
    await server.save()
    
    return UPDATE_SERVER_SECRET_RESPONSE(success=True)