# FastAPI imports
from typing import Optional
from fastapi import FastAPI, APIRouter, Depends, HTTPException, Request
import pydantic
import jsend
from app.models.data_process_type import get_data_process_type

router = APIRouter(tags=["processtypes"])

@router.get("/processtypes")
async def get_data_process_types(request: Request, Depends(get_data_process_type)):
    db_conn = request.app.state.db_conn
    results = get_data_process_type(db_conn=db_conn)
    # data_process_types = get_data_process_type(data_process_type, request.state.db_conn)
    return jsend.success({f"data_process_type": {results}})


@router.get("/processtypes/{process_type}")
async def get_data_process_types(request: Request, process_type: str | None = None):
    # data_process_types = get_data_process_type(data_process_type, request.state.db_conn)
    return jsend.success({f"message": "Data process type retrieved successfully"})
    # if not data_process_type:
    #     jsend.success({"message": "Data process type not found"})
    # else: 
    #     jsend.success({"data_process_type": "{data_process_types}"})


@router.post("/processtypes")
async def create_data_process_type(request: Request):
    return jsend.success({f"message": "Item created", "item": ""})