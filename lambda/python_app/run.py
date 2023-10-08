from logging import Logger, getLogger
import logging
from argparse import ArgumentParser
from tools import (
    validate_env_vars
)


arg_parser = ArgumentParser("Fitness Application")

arg_parser.add_argument("-d", "--debug", help="Debug mode", action="store_true")
arg_parser.add_argument("-c", "--config", help="TOML formated configuration.")
arg_parser.add_argument("-H", "--host", default="0.0.0.0", help="Host to run the web server on")
arg_parser.add_argument("-p", "--port", default=8080, type=int, help="Port to run the web server on")
arg_parser.add_argument("-l", "--log", help="Log file")
arg_parser.add_argument("-v", "--verbose", help="Verbose mode", action="store_true")

## Database connection arguments
arg_parser.add_argument("--db_user", help="Database user")
arg_parser.add_argument("--db_pass", help="Database password")
arg_parser.add_argument("--db_host", help="Database host")
arg_parser.add_argument("--db_port", help="Database port")
arg_parser.add_argument("--db_name", help="Database name")
arg_parser.add_argument("--db_engine", help="Database engine")

## Secret key argument
arg_parser.add_argument("--secret_key", help="Secret key")

args = arg_parser.parse_args()



## Setup logging based on the parsed arguments
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
logger: Logger = getLogger(__name__)

if args.log:
    logging_handler = logging.FileHandler(args.log)
else:
    logging_handler = logging.StreamHandler()

if args.verbose:
    logging_handler.setLevel(logging.INFO)
    logger.setLevel(logging.INFO)
if args.debug:
    logging_handler.setLevel(logging.DEBUG)
    logger.setLevel(logging.DEBUG)

logging_handler.setFormatter(formatter)
logger.addHandler(logging_handler)

validate_env_vars(args)


logger.info("Importing Fitness Module")

from waitress import serve

try:
    from Fitness import app
    logger.info("Starting Fitness application")
    serve(app, host=args.host, port=args.port)
except Exception as e:
    logger.error(e, exc_info=True)
