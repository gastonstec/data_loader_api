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
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    root_path: str = ""
    base_url: str = "/api/v1"

# Database settings
class DBSettings:
    user: str = "postgres"
    password: str = "c4rec4"
    # host: str = "localhost"
    host: str = "147.182.190.223"
    port: int = 5432
    dbname: str = "gtim_services"
    appname: str = "DataLoaderAPI"
    min_size: int = 1
    max_size: int = 5
    timeout_qry: float = 5.0
    timeout_conn: float = 45.0

    def is_valid(self) -> bool:
        # Validate the database settings.
        if not self.user or not self.password or not self.host or not self.dbname:
            return False
        if not isinstance(self.port, int) or self.port <= 0:
            return False
        if not isinstance(self.min_size, int) or self.min_size < 0:
            return False
        if not isinstance(self.max_size, int) or self.max_size <= 0:
            return False
        if self.min_size > self.max_size:
            return False
        return True