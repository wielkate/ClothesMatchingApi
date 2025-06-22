import logging

import psycopg2

from commons.constants import (
    SQL_CREATE_CLOTHES_TABLE,
    SQL_GET_ALL_CLOTHES_ITEMS,
    SQL_INSERT_INTO_CLOTHES_TABLE,
    SQL_UPDATE_CLOTHES_TABLE,
    SQL_DELETE_FROM_CLOTHES_TABLE, DATABASE_PARAMS
)

logger = logging.getLogger(__name__)


def connect():
    return psycopg2.connect(**DATABASE_PARAMS)


def prepare_clothes() -> None:
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(SQL_CREATE_CLOTHES_TABLE)
            connection.commit()
    logger.info(f"Connected to PostgreSQL database")


def load_clothes() -> list[tuple]:
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(SQL_GET_ALL_CLOTHES_ITEMS)
            records = cursor.fetchall()
    logger.info(f"Loaded {len(records)} clothes items from database")
    return records


def add(filename: str, dominant_color: str) -> None:
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(SQL_INSERT_INTO_CLOTHES_TABLE, (filename, dominant_color))
            connection.commit()
    logger.info(f"Added file {filename} with color {dominant_color} to database")


def edit(filename: str, new_color_name: str) -> None:
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(SQL_UPDATE_CLOTHES_TABLE, (new_color_name, filename))
            connection.commit()
    logger.info(f"Updated file {filename} color to {new_color_name} in database")


def delete(filename: str) -> None:
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(SQL_DELETE_FROM_CLOTHES_TABLE, (filename,))
            connection.commit()
    logger.info(f"Deleted file {filename} from database")
