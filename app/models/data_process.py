from pydantic import BaseModel

class DataProcess(BaseModel):
    process_id: str 
    data_process_type: str
    process_date: pydantic.datetime.datetime
    record_count: int
    data_source_uri: str
    other_info: dict
    created_at: pydantic.datetime.datetime
    updated_at: pydantic.datetime.datetime

