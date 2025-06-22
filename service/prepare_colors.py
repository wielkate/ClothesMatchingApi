import csv
import logging

import psycopg2

from commons.constants import COLORS_CSV, SQL_CREATE_COLORS_TABLE, SQL_INSERT_INTO_COLORS_TABLE, DATABASE_PARAMS

logger = logging.getLogger(__name__)


def get_colors_from_csv():
    file = open(file=COLORS_CSV, mode='r', encoding='utf-8')
    return [
        [row[0], int(row[1]), int(row[2]), int(row[3])]
        for row in csv.reader(file, delimiter=',')
    ]


def save_colors_to_database(data: list):
    with psycopg2.connect(**DATABASE_PARAMS) as connection:
        with connection.cursor() as cursor:
            cursor.execute(SQL_CREATE_COLORS_TABLE)
            cursor.executemany(SQL_INSERT_INTO_COLORS_TABLE, data)
        connection.commit()
        logger.info(f"Saved {len(data)} colors to database")


def prepare_colors():
    save_colors_to_database(get_colors_from_csv())
