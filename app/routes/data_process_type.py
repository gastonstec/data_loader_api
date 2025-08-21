# app/routes/data_process_type.py
# FastAPI
from fastapi import APIRouter, Request
# JSON
import json
# Models
from app.models.data_process_type import get_all, get_by_id, create
# JSend response format
import jsend


# Constants
DATA_PROCESS_TYPES = "data_process_types"

# Create a router for the API
router = APIRouter(prefix="/api/v1/processtypes", tags=["Data Process Types"])


# Get all data process types
@router.get("/")
async def get_data_process_types(request: Request):
    try:
        db_conn = request.app.state.db_conn
        results = get_all(db_conn=db_conn)
        return jsend.success({DATA_PROCESS_TYPES: results})
    except Exception as e:
        return jsend.error({"message": str(e)})


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
            return jsend.fail({"message": "Data process type not found"})
        else:
            return jsend.success({DATA_PROCESS_TYPES: results})
    except Exception as e:
        return jsend.error({"message": str(e)})


# Create a new process type
@router.post("/")
async def post_data_process_type(
    request: Request
):
    try:
        # Get and check body contents
        body = await request.body()
        if not body or len(body) == 0:
            return jsend.fail({"message": "Invalid body data"})
        
        # Parse the JSON body of the request
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            return jsend.fail({"message": "Invalid JSON body"})

        # Get the database connection from the request state
        db_conn = request.app.state.db_conn

        # Create the new data process types
        try:
            results = create(db_conn=db_conn, data=data)
        except Exception as e:
            return jsend.error({"message": str(e)})

        # Return the created data process types
        return jsend.success({DATA_PROCESS_TYPES: results})
    except Exception as e:
        return jsend.error({"message": str(e)})
