from pydantic import BaseModel

class DataProcessType(BaseModel): 
    data_process_type: str
    description: str
    table_prefix: str
    source_table_template: str
    destination_table_name: str
    other_info: dict
    created_at: pydantic.datetime.datetime
    updated_at: pydantic.datetime.datetime

class DataProcess(BaseModel):
    process_id: str 
    data_process_type: str
    process_date: pydantic.datetime.datetime
    record_count: int
    data_source_uri: str
    other_info: dict
    created_at: pydantic.datetime.datetime
    updated_at: pydantic.datetime.datetime

