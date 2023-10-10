import os
import sys
import logging


logger = logging.getLogger("Fitness")

def evaluate_env_vars(args: dict) -> None:
    """
        Validates the database arguments.
        Command line arguments will always be used regardless of the set environmental variables
    """
    if not args.db_user:
        args.db_user = os.environ.get('DB_USER')
    if not args.db_pass:
        args.db_pass = os.environ.get('DB_PASSWORD')
    if not args.db_host:
        args.db_host = os.environ.get('DB_HOST')
    if not args.db_port:
        args.db_port = os.environ.get('DB_PORT')
    if not args.db_name:
        args.db_name = os.environ.get('DB_NAME')
    if not args.db_engine:
        args.db_engine = os.environ.get('DB_ENGINE')
    if not args.secret_key:
        args.secret_key = os.environ.get('SECRET_KEY')

    return args