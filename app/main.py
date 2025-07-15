
# Configuration imports
from app.config import AppSettings, DBSettings
# Logging imports
from loguru import logger
# Jsend for structured responses
import jsend
# Database imports
from app.database.db import DBConnection
# FastAPI imports
from fastapi import Depends, FastAPI
from fastapi.routing import APIRoute
from contextlib import asynccontextmanager
# clearfrom fastapi import APIRouter
# from .dependencies import get_query_token, get_token_header
from app.routes.system import router as system_router
# from typing import Optional

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
        
        db_conn = DBConnection(user=db_settings.user, password=db_settings.password, host=db_settings.host, \
                                 port=db_settings.port, dbname=db_settings.dbname, appname=db_settings.appname, \
                                 min_size=db_settings.min_size, max_size=db_settings.max_size, timeout=db_settings.timeout)
        # Connect to the database        
        logger.info("Creating database connection...")
        db_conn.connect()
        db_version = db_conn.test()
        # Log the successful connection
        logger.info(f"Database connection established successfully. Version: {db_version}")
        # Return the connection pool
        return db_conn
    except ValueError as e:
        raise ValueError(f"Failed to create database connection: {e}")

# FastAPI lifespan events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup lifespan event handler
    logger.info(f"Starting up {app.title} v{app.version} application...")
    
    # Connect to the database
    db_conn = connect_to_db()
    if db_conn is None:
        logger.error("Failed to connect to the database during startup.")
        raise RuntimeError("Database connection failed")
    
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
        db_conn.close()
        app.state.db_conn = None  # Clear the pool from app state
        logger.info("Database connection closed successfully.")
    except Exception as e:
        logger.error(f"Error closing connection pool: {e}")

# Create FastAPI app with lifespan events
app = FastAPI(lifespan=lifespan)
# app = FastAPI(lifespan=lifespan, dependencies=[Depends(get_query_token)])

# Include the configuration settings in the app metadata
app.title = AppSettings.name
app.version = AppSettings.version
app.description = AppSettings.description
# Include routers
app.include_router(system_router, prefix=AppSettings.base_url)


# Root endpoint for health check
@app.get("/")
async def root():
    return jsend.success({'message':'OK'})








