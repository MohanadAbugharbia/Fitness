from logging import Logger, getLogger
import logging
from paste.translogger import TransLogger
from argparse import ArgumentParser
import sys
from tools import (
    evaluate_env_vars,
    parse_database_config,
    parse_application_config,
)


arg_parser = ArgumentParser("Fitness Application")

general_args = arg_parser.add_argument_group("General arguments")
general_args.add_argument("-d", "--debug", help="Debug mode", action="store_true")
general_args.add_argument("-c", "--config", help="TOML formated configuration.")
general_args.add_argument("-l", "--log", help="Log file")

## Database connection arguments
db_args = arg_parser.add_argument_group("Database connection arguments")
db_args.add_argument("--db_user", help="Database user")
db_args.add_argument("--db_pass", help="Database password")
db_args.add_argument("--db_host", help="Database host")
db_args.add_argument("--db_port", help="Database port")
db_args.add_argument("--db_name", help="Database name")
db_args.add_argument("--db_engine", help="Database engine", choices=["postgressql"])

## Secret key argument
app_args = arg_parser.add_argument_group("Application arguments")
app_args.add_argument("-H", "--host", default="0.0.0.0", help="Host to run the web server on. Default: 0.0.0.0")
app_args.add_argument("-p", "--port", default=8080, type=int, help="Port to run the web server on. Default: 8080")
app_args.add_argument("--secret_key", help="Secret key")

args = arg_parser.parse_args()
args = evaluate_env_vars(args)


## Setup logging based on the parsed arguments
logger: Logger = getLogger("Fitness")

if args.log:
    logging_handler = logging.FileHandler(args.log)
else:
    logging_handler = logging.StreamHandler()

logging_handler.setLevel(logging.INFO)
logger.setLevel(logging.INFO)

if args.debug:
    logging_handler.setLevel(logging.DEBUG)
    logger.setLevel(logging.DEBUG)

logger.addHandler(logging_handler)

db_conf = parse_database_config(args)
app_conf = parse_application_config(args)


logger.info("Importing Fitness Module")

from waitress import serve

try:
    from Fitness import create_app
    logger.info("Starting Fitness application")
    app = create_app(db_conf, app_conf)
    serve(TransLogger(app, logger=logger, setup_console_handler=False), host=args.host, port=args.port)
except Exception as e:
    logger.error(e, exc_info=True)
    sys.exit(-1)
