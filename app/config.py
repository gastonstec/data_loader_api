# Environment settings
class EnvSettings:
    debug: bool = False
    env: str = "dev"
    db_connect: bool = True
    log_level: str = "DEBUG"
    log_file: str = "app.log"

# Application settings
class AppSettings:
    name: str = "DataLoaderAPI"
    version: str = "1.0.0"
    description: str = "Data Loader API for GTIM Services"
    host: str = "localhost"
    port: int = 8000
    root_path: str = ""
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    root_path: str = "/"
    base_url: str = "/api/v1"

# Database settings
class DBSettings:
    user: str = "postgres"
    password: str = "c4rec4"
    host: str = "localhost"
    port: int = 5432
    dbname: str = "gtim_services"
    appname: str = "MyFastAPIApp"
    min_size: int = 3
    max_size: int = 15
    timeout: int = 30