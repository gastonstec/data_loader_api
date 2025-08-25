from psycopg import rows, Cursor
import json
from app.core.database import DBConnectionPool


# Constants
QRY_SELECT_ALL = (
    "SELECT data_process_type, description, table_prefix, "
    "source_table_template, destination_table_name, "
    "other_info, created_at, updated_at "
    "FROM data_process_type ORDER BY data_process_type"
)

QRY_SELECT_IN = (
    "SELECT data_process_type, description, table_prefix, "
    "source_table_template, destination_table_name, "
    "other_info, created_at, updated_at "
    "FROM data_process_type "
    "WHERE data_process_type = ANY (%s) "
    "ORDER BY data_process_type"
)

QRY_SELECT_BY_ID = (
    "SELECT data_process_type, description, table_prefix, "
    "source_table_template, destination_table_name, "
    "other_info, created_at, updated_at "
    "FROM data_process_type WHERE data_process_type = %s"
)

QRY_INSERT = (
    "INSERT INTO data_process_type (data_process_type, description, "
    "table_prefix, source_table_template, destination_table_name, other_info) "
    "VALUES (%s, %s, %s, %s, %s, %s)"
)


# Select multiple data process types
def _select_in(
    cur: Cursor,
    data_process_types: list[str]
) -> list[dict]:
    try:
        qrystr = QRY_SELECT_IN
        cur.execute(qrystr, (data_process_types,))
        rows = cur.fetchall()
        return [dict(row) for row in rows]
    except Exception as e:
        raise ValueError(e)


# Get all data process types
def get_all(db_conn: DBConnectionPool) -> list[dict]:
    try:
        # Get a connection from the pool
        conn = db_conn.get_conn()
        # Check if the connection is valid
        if conn is None:
            raise ValueError("Failed to get a connection from the pool")
        # Execute query
        qrystr = QRY_SELECT_ALL
        with conn.cursor() as cur:
            cur.execute(qrystr)
            rows = cur.fetchall()
        # Return rows
        conn.commit()
        db_conn.put_conn(conn)
        return [dict(row) for row in rows]
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
        qrystr = QRY_SELECT_BY_ID
        with conn.cursor(row_factory=rows.dict_row) as cur:
            cur.execute(qrystr, (data_process_type,))
            result_rows = cur.fetchall()
        # Return rows
        conn.commit()
        db_conn.put_conn(conn)
        if len(result_rows) < 1:
            raise ValueError("data_process_type not found")
        return result_rows[0]
    except Exception as e:
        raise ValueError(e)


# Create a new data process type
def create(db_conn: DBConnectionPool, data: dict) -> list[dict]:

    # Validate input
    try:
        if not isinstance(data, dict):
            raise ValueError("Input data must be a dictionary")
        if 'data_process_types' not in data:
            raise ValueError("data_process_types is required")
    except Exception as e:
        raise ValueError(str(e))

    # Get a connection from the pool
    try:
        # Get a connection from the pool
        conn = db_conn.get_conn()
        # Check if the connection is valid
        if conn is None:
            raise ValueError("Failed to get a connection from the pool")
    except Exception as e:
        raise ValueError(str(e))

    # Execute inserts
    qrystr = QRY_INSERT
    cur = conn.cursor()
    try:
        for dpt in data['data_process_types']:
            # Execute insert
            cur.execute(qrystr, (
                str(dpt['data_process_type']),
                str(dpt['description']),
                str(dpt['table_prefix']),
                str(dpt['source_table_template']),
                str(dpt['destination_table_name']),
                json.dumps(dpt['other_info'])
            ))
        # Get the list of data process types
        dpt_list = [str(dpt['data_process_type']) for dpt
                    in data['data_process_types']]
        # Get the rows for the inserted data process types
        rows = _select_in(cur, dpt_list)
        # Commit changes
        cur.connection.commit()
    except Exception as e:
        cur.connection.rollback()
        raise ValueError(
            f"Error inserting data into data_process_type: {e}"
        )
    finally:
        db_conn.put_conn(conn)
    return [dict(row) for row in rows]
