from psycopg_pool import ConnectionPool
from psycopg import Connection
from psycopg.rows import TupleRow
from pydantic import BaseModel

# Database connection class for managing PostgreSQL connections using psycopg_pool
class DBConnection:
    # Initialize the database connection parameters
    # user: str, password: str, host: str, port: int, dbname: str, \
    # appname: str, min_size: int, max_size: int, timeout: float
    # min_size: Minimum number of connections in the pool
    # max_size: Maximum number of connections in the pool
    # timeout: Timeout for acquiring a connection from the pool in seconds
    def __init__(self, user: str, password: str, host: str, port: int, dbname: str, \
                 appname: str, min_size: int, max_size: int, timeout: float):
        self.user:str = user
        self.password:str = password
        self.host:str = host
        self.port:int = port
        self.dbname:str = dbname
        self.appname:str = appname
        self.min_size:int = min_size
        self.max_size:int = max_size
        self.timeout:float = timeout
        from typing import Optional
        self.pool: ConnectionPool[Connection[TupleRow]]

    # Connect to the database and return a connection pool
    # Returns a ConnectionPool object
    def connect(self):
        # Check pool selfs
        if self.min_size < 0 or self.max_size < 0 or self.timeout < 0:
            raise ValueError("Pool self must be non-negative")
        if self.min_size > self.max_size:
            raise ValueError("Minimum pool size must be less than or equal to maximum pool size")
        if self.min_size > 100 or self.max_size > 100:
            raise ValueError("Pool self must be less than or equal to 100")
        if self.timeout > 60:
            raise ValueError("Timeout must be less than or equal to 60 seconds")
        if self.min_size < 1:
            raise ValueError("Minimum pool size must be greater than or equal to 1")
        
        # Build connection string
        connstr =  f"user={self.user} " \
            f"password={self.password} " \
            f"host={self.host} " \
            f"port={self.port} " \
            f"dbname={self.dbname} " \
            f"application_name='{self.appname}'"
        
        # Create connection pool
        try:
            self.pool: ConnectionPool[Connection[TupleRow]] = \
            ConnectionPool(conninfo=connstr, min_size=self.min_size, max_size=self.max_size, timeout=self.timeout)
        except Exception as e:
            raise ValueError(f"Failed to create connection pool: {e}")

    # Test the connection by executing a simple query
    def test(self) -> str:
        # Check connection
        # conn: Connection[TupleRow] = None
        try:
            # Test connection by executing a simple query
            conn = self.pool.getconn()  # Get a connection from the pool
            if conn is None:
                raise ValueError("Failed to get a connection from the pool")
            with conn.cursor() as cur:
                cur.execute("SELECT version()")
                dbversion = cur.fetchone()
            # Commit changes (if any)
            conn.commit()
            # Return connection to pool
            self.pool.putconn(conn)
        except Exception as e:
            raise ValueError(e)
    
        return str(dbversion)

    # Close connection pool
    def close(self) -> None:
        try:
            self.pool.close()
        except Exception as e:
            raise ValueError(e)
        return
