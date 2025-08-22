# app/routes/data_process_type.py
# FastAPI
from fastapi import APIRouter, Request
# JSON
import json
# Models
from app.models.data_process_type import get_all, get_by_id, create
# Application imports
from app.core import jsend_success, jsend_error, jsend_fail
# Logging imports
from loguru import logger


# Constants
DATA_PROCESS_TYPES = "data_process_types"

# Create a router for the API
router = APIRouter(prefix="/api/v1/processtypes", tags=["Data Process Types"])


# Get all data process types
@router.get("")
async def get_data_process_types(request: Request):
    try:
        db_conn = request.app.state.db_conn
        results = get_all(db_conn=db_conn)
        return jsend_success(data={DATA_PROCESS_TYPES: results})
    except Exception as e:
        logger.error(f"Error getting process types: {e}")
        return jsend_error(
            message=f"Error getting process types: {e}",
            code=500
        )


# Get a specific process type
@router.get("/{data_process_type}")
async def get_data_process_type(
    request: Request,
    data_process_type: str
):
    try:
        # Get the database connection from the request state
        db_conn = request.app.state.db_conn
        # Get the data process type by ID
        results = get_by_id(
            db_conn=db_conn, data_process_type=data_process_type
        )
        # Check if the process type was found
        if not results:
            return jsend_fail(
                message=f"Data process type {data_process_type} not found"
            )
        else:
            return jsend_success(data={DATA_PROCESS_TYPES: results})
    except Exception as e:
        logger.error(f"Error getting process type: {e}")
        return jsend_error(message=f"Error getting process type: {e}")


# Create a new process type
@router.post("")
async def post_data_process_type(
    request: Request
):
    try:
        # Get and check body contents
        body = await request.body()
        if not body or len(body) == 0:
            return jsend_fail(message="Invalid body data")

        # Parse the JSON body of the request
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            return jsend_fail(message="Invalid JSON body")

        # Get the database connection from the request state
        db_conn = request.app.state.db_conn

        # Create the new data process types
        try:
            results = create(db_conn=db_conn, data=data)
        except Exception as e:
            return jsend_error(
                message="Error creating data process types",
                data={"error": str(e)}
            )
        # Return the created data process types
        return jsend_success({DATA_PROCESS_TYPES: results})
    except Exception as e:
        return jsend_error(
                message="Error creating data process types",
                data={"error": str(e)}
            )
