from pydantic.main import BaseModel
from datetime import datetime


# Pydantic model for data process type
class DataProcessType(BaseModel):
    data_process_type: str
    description: str
    table_prefix: str
    source_table_template: str
    destination_table_name: str
    other_info: dict
    created_at: datetime
    updated_at: datetime

    def validate_fields(self) -> bool:
        # Check data process type
        if (
            not self.data_process_type
            or len(self.data_process_type) < 1
            or len(self.data_process_type) > 25
        ):
            raise ValueError("data_process_type value is invalid")
        # Check description
        if (
            not self.description
            or len(self.description) < 2
        ):
            raise ValueError("description value is invalid")
        # Check table prefix
        if len(self.table_prefix) > 15:
            raise ValueError("table_prefix value is invalid")
        # Check source table template
        if (
            len(self.source_table_template) < 15
        ):
            raise ValueError("source_table_template value is invalid")
        return True