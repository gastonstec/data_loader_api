from fastapi import APIRouter


router = APIRouter(prefix="/dataprocesses", tags=["dataprocesses"])

@router.get("/{process_id}")
async def get_processes():
    return [{"name": "Item 1"}, {"name": "Item 2"}]

@router.post("/")
async def create_process(item: dict):
    return {"message": "Item created", "item": item}