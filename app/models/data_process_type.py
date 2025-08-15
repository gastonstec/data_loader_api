import psycopg
from app.core.database import DBConnectionPool
from app.schemas.data_process_type import DataProcessType


# Get all data process types
def get_all(db_conn: DBConnectionPool) -> list[dict]:
    try:
        # Get a connection from the pool
        conn = db_conn.get_conn()
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
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute(qrystr)
            rows = cur.fetchall()
        # Return rows
        conn.commit()
        db_conn.put_conn(conn)
        return rows
    except Exception as e:
        raise ValueError(e)


# Create a new data process type
def create(db_conn: DBConnectionPool, data: dict) -> bool:
    try:
        # Validate input
        if not data:
            raise ValueError("data_process_type is required")

        # Get a connection from the pool
        conn = db_conn.get_conn()
        # Check if the connection is valid
        if conn is None:
            raise ValueError("Failed to get a connection from the pool")

        # Prepare data for insertion
        datalist: list[DataProcessType] = data
        # Execute insert
        for item in datalist:
            # Build query
            qrystr = (
                "INSERT INTO data_process_type (data_process_type, "
                "description, table_prefix, source_table_template, "
                "destination_table_name, other_info) "
                "VALUES (%s, %s, %s, %s, %s, %s)"
            )
            # Execute insert
            with conn.cursor() as cur:
                cur.execute(qrystr, (
                    str(item.get("data_process_type")),
                    str(item.get("description")),
                    str(item.get("table_prefix")),
                    str(item.get("source_table_template")),
                    str(item.get("destination_table_name")),
                    str(item.get("other_info"))
                ))
        # Commit changes
        conn.commit()
        # Close connection
        db_conn.put_conn(conn)
        return True
    except Exception as e:
        raise ValueError(e)


# Get a specific process type
def get_by_id(
    db_conn: DBConnectionPool,
    data_process_type: str
) -> dict:
    try:
        # Get a connection from the pool
        conn = db_conn.get_conn()
        # Check if the connection is valid
        if conn is None:
            raise ValueError("Failed to get a connection from the pool")
        # Execute query
        qrystr = (
            "SELECT data_process_type, description, table_prefix,"
            "source_table_template, destination_table_name,"
            "other_info, created_at, updated_at "
            "FROM data_process_type WHERE data_process_type = %s"
        )
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute(qrystr, (data_process_type,))
            rows = cur.fetchall()
        # Return rows
        conn.commit()
        db_conn.put_conn(conn)
        return rows
    except Exception as e:
        raise ValueError(e)


# Update a specific process type
def update_by_id(
    db_conn: DBConnectionPool,
    data_process_type: str,
    updates: dict
) -> bool:
    try:
        # Get a connection from the pool
        conn = db_conn.get_conn()
        # Check if the connection is valid
        if conn is None:
            raise ValueError("Failed to get a connection from the pool")
        # Execute update
        qrystr = (
            "UPDATE data_process_type SET "
            "description = %s, table_prefix = %s, "
            "source_table_template = %s, destination_table_name = %s, "
            "other_info = %s, created_at = %s, updated_at = %s "
            "WHERE data_process_type = %s"
        )
        with conn.cursor() as cur:
            cur.execute(qrystr, (
                updates.get("description"),
                updates.get("table_prefix"),
                updates.get("source_table_template"),
                updates.get("destination_table_name"),
                updates.get("other_info"),
                updates.get("created_at"),
                updates.get("updated_at"),
                data_process_type
            ))
        # Commit changes
        conn.commit()
        db_conn.put_conn(conn)
        return True
    except Exception as e:
        raise ValueError(e)

        # Get a connection from the pool
        conn = db_conn.get_conn()
        # Check if the connection is valid
        if conn is None:
            raise ValueError("Failed to get a connection from the pool")
        # Execute query
        qrystr = (
            "SELECT data_process_type, description, table_prefix,"
            "source_table_template, destination_table_name,"
            "other_info, created_at, updated_at "
            "FROM data_process_type WHERE data_process_type = %s"
        )
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute(qrystr, (data_process_type,))
            rows = cur.fetchall()
        # Return rows
        conn.commit()
        db_conn.put_conn(conn)
        return rows
    except Exception as e:
        raise ValueError(e)
