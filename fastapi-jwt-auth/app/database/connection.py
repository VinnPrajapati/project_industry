import sys
from pathlib import Path
from urllib.parse import quote_plus

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent

sys.path.append(str(ROOT_DIR))

from sqlalchemy import create_engine

from shared.config_loader import get_mysql_master

mysql = get_mysql_master()

password = quote_plus(mysql["password"])

DATABASE_URL = (
    f"mysql+pymysql://"
    f"{mysql['username']}:{password}@"
    f"{mysql['host']}:{mysql['port']}/"
    f"{mysql['database']}"
)

print("this is database url",DATABASE_URL)

engine = create_engine(
    DATABASE_URL,

    echo=True,

    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True
)