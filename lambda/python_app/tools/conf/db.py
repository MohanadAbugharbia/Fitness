from pydantic import BaseModel

class DatabaseConfig(BaseModel):
    user: str
    password: str
    host: str
    port: int
    database: str
    engine: str

    def __repr__(self) -> str:
        return f"DatabaseConfig(user={self.user}, host={self.host}, port={self.port}, database={self.database}, engine={self.engine})"
    def __str__(self) -> str:
        return self.__repr__()

def parse_database_args(args) -> DatabaseConfig:
    """
        Parses the database arguments and returns a DatabaseConfig object.
    """
    db_conf = DatabaseConfig(
        user=args.db_user,
        password=args.db_pass,
        host=args.db_host,
        port=args.db_port,
        database=args.db_name,
        engine=args.db_engine,
    )
    return db_conf  
