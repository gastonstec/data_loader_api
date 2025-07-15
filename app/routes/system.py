
from typing import Any
# Import FastAPI and necessary modules
from fastapi import FastAPI, APIRouter, Depends, HTTPException, Request
# Jsend for structured responses
import jsend
from app.database import DBConnection
# from .deps import SessionDep

# Create a FastAPI router for system-related endpoints
router = APIRouter(prefix="/sys", tags=["system"])

# Get database version
@router.get("/db", summary="Get Database Version")
async def dbversion(request: Request) -> Any:
    db_conn: DBConnection = request.app.state.db_conn
    db_version= db_conn.test()
    print(f"Database version: {db_version}")
    return jsend.success({f"db_version": {db_version}})