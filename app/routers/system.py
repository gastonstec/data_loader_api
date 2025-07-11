
# Import FastAPI and necessary modules
from fastapi import FastAPI, APIRouter, Depends, HTTPException
from ..dependencies import get_token_header
# Database imports
from ..database import DBConnection
# Jsend for structured responses
import jsend

# Create a FastAPI router for system-related endpoints
router = APIRouter(
    prefix="/sys",
    tags=["system"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

# Get database version
@router.get("/dbver")
async def db_version(app: FastAPI):
    try:
        db_version = app.state.db_conn.test()
    except Exception as e:
        jsend.error({'message': {str(e)}})
    return jsend.success({'database': {db_version}})