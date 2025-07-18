from pydantic import BaseModel
from app.database.db import DBConnectionPool

class DataProcessType(BaseModel): 
    self.data_process_type: str
    self.description: str
    self.table_prefix: str
    self.source_table_template: str
    self.destination_table_name: str
    self.other_info: dict
    self.created_at: pydantic.datetime.datetime
    self. updated_at: pydantic.datetime.datetime

    

    def get(data_process_type: str = None, db_conn: DBConnectionPool = None):
    # This function would typically fetch the DataProcessType from a database or other source
    # For now, we return a dummy instance for demonstration purposes
    try:
        # Get a connection from the pool
        conn = db_conn.pool.getconn()
        # Check if the connection is valid
        if conn is None:
            raise ValueError("Failed to get a connection from the pool")    
        # Execute query
        qrystr = "data_process_type, description, table_prefix, source_table_template, destination_table_name, other_info, created_at, updated_at" \
                "from data_process_type order by data_process_type"
        with conn.cursor() as cur:
            cur.execute(qrystr)
            rows = cur.fetchall()
        # Return connection to pool
        self.pool.putconn(conn)
        return rows
    except Exception as e:
        raise ValueError(e)
    