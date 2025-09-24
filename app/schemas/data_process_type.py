from pydantic.main import BaseModel, Optional
from datetime import datetime


# Pydantic model for data process type
class DataProcessType(BaseModel):
    data_process_type: str
    description: str
    table_prefix: str
    destination_table_name: str
    other_info: Optional[dict] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def check_values(self) -> bool:
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
        
        # Check destination table name
        if (
            not self.destination_table_name
            or len(self.destination_table_name) < 1
            or len(self.destination_table_name) > 60
        ):
            raise ValueError("destination_table_name value is invalid")

        return True
