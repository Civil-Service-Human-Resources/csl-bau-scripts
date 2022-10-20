import logging
import sys
from dotenv import load_dotenv
import os

load_dotenv()

log_formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger()
logger.level = logging.INFO

file_log = logging.FileHandler(filename="logs.txt")
file_log.setFormatter(log_formatter)
logger.addHandler(file_log)

console_log = logging.StreamHandler(sys.stdout)
console_log.setFormatter(log_formatter)
logger.addHandler(console_log)

def get_sql_conn(database):

    return {
        "user" :os.environ['SQL_USER'],
        "password" :os.environ['SQL_PASSWORD'],
        "host" :os.environ['SQL_HOST'],
        "port" :os.environ['SQL_PORT'],
        "database": database,
        "ssl_ca": f"{os.path.dirname(__file__)}/../supporting_files/BaltimoreCyberTrustRoot.crt.pem"
    }
