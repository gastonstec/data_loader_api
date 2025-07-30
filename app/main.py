
# Configuration imports
from app.config import AppSettings, DBSettings
# Logging imports
from loguru import logger
# Database imports
from app.database.db import DBConnectionPool
# FastAPI imports
from fastapi import Depends, FastAPI
from fastapi.routing import APIRoute
from contextlib import asynccontextmanager
# Router imports
from app.routes.system import router as system_router
from app.routes.data_process_type import router as data_process_type_router


# Create database connection pool
def create_db_pool():
    """
    Create a database connection pool using the provided settings.
    """
    # Load database settings from the environment
    db_settings = DBSettings()

    # Validate the database settings    
    if not db_settings.is_valid():
        raise ValueError("Invalid database settings provided.")
    
    # Log the connection details
    logger.info(f"Connecting to database {db_settings.dbname} at {db_settings.host}:{db_settings.port}")

    # Create a database connection pool
    db_conn = DBConnectionPool(user=db_settings.user, password=db_settings.password, host=db_settings.host, \
                                    port=db_settings.port, dbname=db_settings.dbname, appname=db_settings.appname, \
                                    min_size=db_settings.min_size, max_size=db_settings.max_size, timeout=DBSettings.timeout_conn)

    return db_conn

# Initialize the database connection pool
try:
    db_conn = create_db_pool()
except Exception as e:
    logger.error(f"Failed to create database connection pool: {e}")
    raise RuntimeError(f"Database connection pool creation failed: {e}")

# Connect to the database and return the connection pool.
def connect_to_db(db_conn: DBConnectionPool):
    try:
        # Connect to the database        
        logger.info("Creating database connection...")
        db_conn.connect(timeout=DBSettings.timeout_conn)
        db_version = db_conn.test()
        # Log the successful connection
        logger.info(f"Database connection established successfully. Version: {db_version}")
        return
    except Exception as e:
        raise e  # Re-raise the exception to be handled in the lifespan event


# FastAPI lifespan events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup lifespan event handler
    logger.info(f"Starting up {app.title} v{app.version} application...")
    
    # Connect to the database
    try:
        connect_to_db(db_conn)
        if db_conn is None:
            logger.error("Failed to connect to the database during startup.")
            raise RuntimeError("Database connection failed")
    except Exception as e:
        logger.error(f"Error occurred during database connection: {e}")
        raise RuntimeError(f"Database connection failed during startup: {e}")
    
    # Store the connection pool in the app state
    app.state.db_conn = db_conn

    # Yield control back to FastAPI
    yield

    # Shutdown lifespan event handler
    logger.info(f"Shutting down {app.title} v{app.version} application...")

    # Ensure the connection pool is closed properly
    if not hasattr(app.state, 'db_conn'):
        logger.warning("No database connection found in app state during shutdown.")
        return
    
    # Close the connection pool
    logger.info("Closing the database connection pool...")
    try:
        # Close the connection pool
        db_conn.close(timeout=DBSettings.timeout_conn)
        app.state.db_conn = None  # Clear the pool from app state
        logger.info("Database connection closed successfully.")
    except Exception as e:
        logger.error(f"Error closing connection pool: {e}")

    return

# Create FastAPI app
app = FastAPI(lifespan=lifespan, title=AppSettings.name, version=AppSettings.version, description=AppSettings.description)

# Include routers
app.include_router(system_router, prefix=AppSettings.base_url)
app.include_router(data_process_type_router, prefix=AppSettings.base_url)

# Root endpoint for health check
@app.get("/")
async def root():
    return ({'App Name': AppSettings.name, 'Version': AppSettings.version, 'Description': AppSettings.description})
