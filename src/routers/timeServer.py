from fastapi import APIRouter
import datetime as dt

router = APIRouter()


# Todo: Add error handing

@router.get("/time")
async def get_time():
    return {"time": dt.datetime.now() }







