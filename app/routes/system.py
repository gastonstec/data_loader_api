
# app/routes/system.py
# This module defines system-related endpoints for the FastAPI application.
# 
# FastAPI imports
from fastapi import FastAPI, APIRouter, Depends, HTTPException, Request
# jsend is a library for creating JSON responses with a consistent structure
import jsend

# Create FastAPI router for system-related endpoints
router = APIRouter(tags=["system"])

# Get database version
@router.get("sys/dbver", summary="Get Database Version")
async def db_version(request: Request):
    # Get the database version
    db_version= request.app.state.db_conn.test()
    return jsend.success({f"db_version": {db_version}})

# Get database stats
@router.get("sys/dbinfo", summary="Get Database connection Stats")
async def db_conn_info(request: Request):
    # Get the database connection pool from the app state
    pool = request.app.state.db_conn.pool
    return jsend.success({f"connection_stats": {str(pool.get_stats())}})