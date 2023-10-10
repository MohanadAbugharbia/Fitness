from pydantic import BaseModel


class ApplicationConfig(BaseModel):
    secret_key: str


def parse_application_config(args) -> ApplicationConfig:
    """
        Parses the application arguments and returns an ApplicationConfig object.
    """
    app_conf = ApplicationConfig(secret_key=args.secret_key)
    return app_conf