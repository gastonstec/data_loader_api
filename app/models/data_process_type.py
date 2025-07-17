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

def get_data_process_type(data_process_type: str, db_conn: D) -> DataProcessType:
    # This function would typically fetch the DataProcessType from a database or other source
    # For now, we return a dummy instance for demonstration purposes
    return DataProcessType(
        data_process_type=data_process_type,
        description="Sample description",
        table_prefix="prefix_",
        source_table_template="source_template",
        destination_table_name="destination_table",
        other_info={},
        created_at=pydantic.datetime.datetime.now(),
        updated_at=pydantic.datetime.datetime.now()
    )