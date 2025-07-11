
# Configuration imports
from config import EnvSettings, AppSettings, DBSettings
# Logging imports
from loguru import logger
# Database imports
from database import PoolSettings, connect, close, test_connection
# FastAPI imports
from fastapi import FastAPI
from contextlib import asynccontextmanager
# FastAPI routers


# Connect to the database and return the connection pool.
def connect_to_db():
    try:
        # Load database settings from the environment
        db_settings = DBSettings()

        # Validate the database settings    
        if not db_settings.is_valid():
            raise ValueError("Invalid database settings provided.")
        
        # Log the connection details
        logger.info(f"Connecting to database {db_settings.dbname} at {db_settings.host}:{db_settings.port}")
        
        # Create the connection settings
        pool_settings = PoolSettings(user=db_settings.user, password=db_settings.password, host=db_settings.host, \
                                port=db_settings.port, dbname=db_settings.dbname, appname=db_settings.appname, \
                                min_size=db_settings.min_size, max_size=db_settings.max_size, timeout=db_settings.timeout)
        # Create the connection
        logger.info("Creating database connection...")
        conn_pool = connect(settings=pool_settings)
        db_version = test_connection(conn_pool)
        logger.info("Database connection created successfully: {db_version}")
        return conn_pool
    except ValueError as e:
        logger.error(f"Failed to create database connection: {e}")
        return None

# FastAPI lifespan events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup lifespan event handler
    logger.info("Starting up the FastAPI application...")
    
    # Connect to the database
    conn_pool = connect_to_db()
    if conn_pool is None:
        logger.error("Failed to connect to the database during startup.")
        raise RuntimeError("Database connection failed")
    
    # Store the connection pool in the app state
    app.state.conn_pool = conn_pool

    yield       # Yield control back to FastAPI

    # Shutdown lifespan event handler
    logger.info("Shutting down the FastAPI application...")

    # Ensure the connection pool is closed properly
    if not hasattr(app.state, 'conn_pool'):
        logger.warning("No connection pool found in app state during shutdown.")
        return
    
    # Close the connection pool
    logger.info("Closing the database connection pool...")
    try:
        # Close the connection pool
        close(app.state.conn_pool)
        app.state.conn_pool = None  # Clear the pool from app state
        logger.info("Database connection pool closed successfully.")
    except Exception as e:
        logger.error(f"Error closing connection pool: {e}")

# Create FastAPI app with lifespan events
app = FastAPI(lifespan=lifespan)

# Include the configuration settings in the app metadata
app.title = AppSettings.name
app.version = AppSettings.version
app.description = AppSettings.description
app.host = AppSettings.host
app.port = AppSettings.port


# Root endpoint for health check
@app.get("/")
async def root():
    return {f"message":"OK"}

# Get database version
@app.get("/dbversion")
async def dbversion():
    try:
        db_version = test_connection(app.state.conn_pool)
    except Exception as e:
        logger.error(f"Error testing database connection: {e}")
        return {"error": "Database connection failed"}
    return {f"message": {db_version}}

