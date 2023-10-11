from pydantic import BaseModel
from typing import (
    Optional,
    Union,
    Literal,
)


class DatabaseConfig(BaseModel):
    user: str
    password: str
    host: Optional[Literal["localhost"]] = "localhost"
    port: Optional[Literal[5432]] = 5432
    database: str
    engine: Optional[Literal["postgresql"]] = "postgresql"

    def __repr__(self) -> str:
        return f"DatabaseConfig(user={self.user}, host={self.host}, port={self.port}, database={self.database}, engine={self.engine})"
    def __str__(self) -> str:
        return self.__repr__()

def parse_database_config(args) -> DatabaseConfig:
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

