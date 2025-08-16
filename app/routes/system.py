# app/routes/system.py
# This module defines system-related endpoints for the FastAPI application.
#

# FastAPI imports
from fastapi import Request, APIRouter, HTTPException


# Create FastAPI router for system-related endpoints
router = APIRouter(prefix="/sys")


# Get database version
@router.get("/dbver", summary="Get Database Version")
async def db_version(request: Request):
    # Get the database version
    try:
        db_version = request.app.state.db_conn.test()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting database version: {e}"
        )
    return {"db_version": db_version}


# Get database stats
@router.get("/dbinfo", summary="Get Database connection Stats")
async def db_conn_info(request: Request):
    # Get the database connection pool from the app state
    try:
        pool = request.app.state.db_conn.pool
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting database connection pool: {e}"
        )
    return {"connection_stats": str(pool.get_stats())}