# FastAPI
from fastapi import APIRouter, Request
# Models
from app.models.data_process_type import get_all, get_by_id, create
# JSend response format
import jsend

# Create a router for the API
router = APIRouter(prefix="/api/v1/processtypes", tags=["Data Process Types"])


# Get all data process types
@router.get("/")
async def get_data_process_types(request: Request):
    try:
        db_conn = request.app.state.db_conn
        results = get_all(db_conn=db_conn)
        return jsend.success({"data_process_type": results})
    except Exception as e:
        return jsend.error({"message": str(e)})


# Get a specific process type
@router.get("/{data_process_type}")
async def get_data_process_type(
    request: Request,
    data_process_type: str
):
    try:
        db_conn = request.app.state.db_conn
        results = get_by_id(
            db_conn=db_conn, data_process_type=data_process_type
        )
        return jsend.success({"data_process_type": results})
    except Exception as e:
        return jsend.error({"message": str(e)})


# Create a new process type
@router.post("/")
async def create_data_process_type(
    request: Request
):
    try:
        db_conn = request.app.state.db_conn
        data = await request.json()
        results = create(db_conn=db_conn, data=data)
        return jsend.success({"data_process_type": results})
    except Exception as e:
        return jsend.error({"message": str(e)})
