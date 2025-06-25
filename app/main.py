
# Configuration imports
from config import EnvSettings, AppSettings, DBSettings
# Logging imports
from loguru import logger

# Database imports
from database import PoolSettings, connect, close, test_connection

def startup():
     # Load environment settings
    env_settings = EnvSettings()
    logger.info(f"Environment: {env_settings.env}, Debug: {env_settings.debug}")

    # Ensure the logger is configured
    logger.add(sink=f"{env_settings.log_file}", rotation="1 MB", level=f"{env_settings.log_level}", backtrace=True, diagnose=True)
    
    # Load application settings
    app_settings = AppSettings()
    logger.info(f"App Name: {app_settings.name}, Version: {app_settings.version}")

    # Load database settings
    if env_settings.db_connect:
        db_settings = DBSettings()
        logger.info(f"Connecting to database {db_settings.dbname} at {db_settings.host}:{db_settings.port}")

        # Create pool settings
        pool_settings = PoolSettings(
            user=db_settings.user,
            password=db_settings.password,
            host=db_settings.host,
            port=db_settings.port,
            dbname=db_settings.dbname,
            appname=db_settings.appname,
            min_size=db_settings.min_size,
            max_size=db_settings.max_size,
            timeout=db_settings.timeout
        )

        # Connect to the database
        try:
            conn_pool = connect(settings=pool_settings)
        except ValueError as e:
            logger.error(f"Failed to create database connection pool: {e}")
            return    
        logger.info("Database connection pool created successfully.")
        logger.info(f"Pool settings: {conn_pool.connection_class}")

        # Test the connection
        try:
            dbversion = test_connection(pool=conn_pool)
            logger.info(f"Connected to database version: {dbversion}")
        except ValueError as e:
            logger.error(f"Connection failed: {e}")

        # Close the pool
        try:
            close(pool=conn_pool)
        except ValueError as e:
            logger.error(f"Failed to close database connection pool: {e}")
            return
        logger.info("Database connection pool closed.")

startup()
