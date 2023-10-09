import os
import sys
import logging


logger = logging.getLogger("Fitness")

def validate_env_vars(args: dict) -> None:
    """
        Validates the database arguments.
        Command line arguments will always be used regardless of the set environmental variables
    """

    if args.db_user or (not os.environ.get('DB_USER') and args.db_user):
        os.environ["DB_USER"] = args.db_user
    if args.db_pass or (not os.environ.get('DB_PASSWORD') and args.db_pass):
        os.environ["DB_PASSWORD"] = args.db_pass
    if args.db_host or (not os.environ.get('DB_HOST') and args.db_host):
        os.environ["DB_HOST"] = args.db_host
    if args.db_port or (not os.environ.get('DB_PORT') and args.db_port):
        os.environ["DB_PORT"] = args.db_port
    if args.db_name or (not os.environ.get('DB_NAME') and args.db_name):
        os.environ["DB_NAME"] = args.db_name
    if args.db_engine or (not os.environ.get('DB_ENGINE')  and args.db_engine):
        os.environ["DB_ENGINE"] = args.db_engine
    if args.secret_key or (not os.environ.get('SECRET_KEY') and args.secret_key):
        os.environ["SECRET_KEY"] = args.secret_key

    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = os.environ.get('DB_PORT')
    DB_NAME = os.environ.get('DB_NAME')
    DB_ENGINE = os.environ.get('DB_ENGINE')

    SECRET_KEY = os.environ.get('SECRET_KEY')

    if None in [DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, DB_ENGINE]:
        logger.error("Database arguments are missing")
        sys.exit(1)

    if None in [SECRET_KEY]:
        logger.error("Application secret key is missing")
        sys.exit(1)