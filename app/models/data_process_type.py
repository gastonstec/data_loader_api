from pydantic import BaseModel
from datetime import datetime
from app.database.db import DBConnectionPool


class DataProcessType(BaseModel):
    data_process_type: str
    description: str
    table_prefix: str
    source_table_template: str
    destination_table_name: str
    other_info: dict
    created_at: datetime
    updated_at: datetime

    @classmethod
    def get(self, data_process_type: str = None, db_conn: DBConnectionPool = None):
        try:
            # Get a connection from the pool
            conn = db_conn.pool.getconn()
            # Check if the connection is valid
            if conn is None:
                raise ValueError("Failed to get a connection from the pool")    
            # Execute query
            qrystr = (
                "SELECT data_process_type, description, table_prefix, "
                "source_table_template, destination_table_name, "
                "other_info, created_at, updated_at "
                "FROM data_process_type ORDER BY data_process_type"
            )
            with conn.cursor() as cur:
                cur.execute(qrystr)
                rows = cur.fetchall()
            # Return connection to pool
            db_conn.pool.putconn(conn)
            return rows
        except Exception as e:
            raise ValueError(e)
