from fastapi import APIRouter


router = APIRouter(prefix="/dataprocesstypes", tags=["dataprocesstypes"])

@router.get("/{data_process_type}")
async def get_data_process_types():
    return [{"name": "Item 1"}, {"name": "Item 2"}]

@router.post("/")
async def create_data_process_type(data_Proce: dict):
    return {"message": "Item created", "item": item}