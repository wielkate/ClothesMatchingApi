import logging

import psycopg2

from commons.constants import (
    SQL_CREATE_CLOTHES_TABLE,
    DATABASE_PARAMS
)

logger = logging.getLogger(__name__)


def prepare_clothes() -> None:
    with  psycopg2.connect(**DATABASE_PARAMS) as connection:
        with connection.cursor() as cursor:
            cursor.execute(SQL_CREATE_CLOTHES_TABLE)
            connection.commit()
    logger.info(f"Created clothes table")
