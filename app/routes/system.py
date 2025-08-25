# app/routes/system.py
# This module defines system-related endpoints for the FastAPI application.
#

# FastAPI imports
from fastapi import Request, APIRouter
# Application imports
from app.core import jsend_success, jsend_error
# Logging imports
from loguru import logger

# Create FastAPI router for system-related endpoints
router = APIRouter(prefix="/sys")


# Get database version
@router.get("/dbver", summary="Get Database Version")
async def db_version(request: Request):
    # Get the database version
    try:
        db_version = request.app.state.db_conn.test()
    except Exception as e:
        logger.error(f"Error getting database version: {e}")
        return jsend_error(
            message=f"Error getting database version: {e}",
            code=500
        )
    return jsend_success(data={"database_version": db_version})


# Get database stats
@router.get("/dbinfo", summary="Get Database connection Stats")
async def db_conn_info(request: Request):
    # Get the database connection pool from the app state
    try:
        pool = request.app.state.db_conn.pool
        pool_stats = pool.get_stats()
    except Exception as e:
        logger.error(f"Error getting database connection pool stats: {e}")
        return jsend_error(
            message=f"Error getting database connection pool stats: {e}",
            code=500
        )
    return jsend_success(data={"pool_stats": pool_stats})
