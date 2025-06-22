import logging

import psycopg2

from commons.constants import SQL_GET_ALL_COLORS, DATABASE_PARAMS
from models.Color import Color

logger = logging.getLogger(__name__)


def load_colors():
    with psycopg2.connect(**DATABASE_PARAMS) as connection:
        with connection.cursor() as cursor:
            cursor.execute(SQL_GET_ALL_COLORS)
            colors = cursor.fetchall()

    logger.info(f'Loaded {len(colors)} colors from database')
    return [Color(color) for color in colors]


global_colors = load_colors()
