from fastapi import FastAPI
import bcrypt

import src.routers.timeServer as timeServer
import src.routers.kerberosServer as kerberosServer
import src.routers.userServer as userServer

from tortoise.contrib.fastapi import register_tortoise

from src.models import Servers, User

app = FastAPI()

app.include_router(timeServer.router)
app.include_router(kerberosServer.router, prefix="/kerberos")
app.include_router(userServer.router , prefix="/user")



register_tortoise(
    app,
    db_url='mysql://myuser:mypassword@localhost:3306/kerberos',
    modules={'models': ['src.models']},
    generate_schemas=True,
    add_exception_handlers=True,
)


# After ınitiliazing the database
# create user Server in db
# create user Client in db

@app.on_event("startup")
async def startup():
    
    # Add Admin that authorized to update server keys to dv
    # Create Admin if not exists
    _admin = await User.get_or_none(username="admin")
    
    if _admin is None:
        # Create Hashed password
        passwordHash = bcrypt.hashpw("admin".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        await User.create(username="admin", password=passwordHash, isAdministrator=True)
    
    # Create User server if not exists
    _userServer = await Servers.get_or_none(id=1)
    
    if _userServer is None:
        await Servers.create(id=1, name="User Server", secret="secret of the user server")



