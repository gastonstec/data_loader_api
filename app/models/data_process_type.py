import psycopg
import json
from app.core.database import DBConnectionPool
# from app.schemas.data_process_type import DataProcessType


QRY_SELECT_ALL = (
    "SELECT data_process_type, description, table_prefix, "
    "source_table_template, destination_table_name, "
    "other_info, created_at, updated_at "
    "FROM data_process_type ORDER BY data_process_type"
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
    "VALUES (%s, %s, %s, %s, %s, %s) RETURNING created_at, updated_at"
)


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
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute(qrystr)
            rows = cur.fetchall()
        # Return rows
        conn.commit()
        db_conn.put_conn(conn)
        return rows
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
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute(qrystr, (data_process_type,))
            rows = cur.fetchall()
        # Return rows
        conn.commit()
        db_conn.put_conn(conn)
        return rows
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
        return

    try:
        # Get a connection from the pool
        conn = db_conn.get_conn()

        # Check if the connection is valid
        if conn is None:
            raise ValueError("Failed to get a connection from the pool")

        # Execute inserts
        qrystr = QRY_INSERT
        try:
            for dpt in data['data_process_types']:
                # Execute insert
                conn.cursor().execute(qrystr, (
                    str(dpt['data_process_type']),
                    str(dpt['description']),
                    str(dpt['table_prefix']),
                    str(dpt['source_table_template']),
                    str(dpt['destination_table_name']),
                    json.dumps(dpt['other_info'])
                ))
                row = conn.cursor().fetchone()
                dpt['created_at'] = row['created_at']
                dpt['updated_at'] = row['updated_at']

            # Commit changes
            conn.commit()

        except Exception as e:
            conn.rollback()
            raise ValueError(
                f"Error inserting data into data_process_type: {e}"
            )
    except Exception as e:
        raise ValueError({"message": str(e)})
        return
    finally:
        # Release connection to the pool
        db_conn.put_conn(conn)
    return data


# Update a specific process type
def update(
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
