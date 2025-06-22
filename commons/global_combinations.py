import logging
from collections import defaultdict

import psycopg2

from commons.constants import DATABASE_PARAMS, SQL_GET_COMBINATIONS_BY_MODE
from models.Mode import Mode

logger = logging.getLogger(__name__)


def load_combinations(mode):
    with psycopg2.connect(**DATABASE_PARAMS) as connection:
        with connection.cursor() as cursor:
            cursor.execute(SQL_GET_COMBINATIONS_BY_MODE, (mode,))
            grouped = defaultdict(list)
            for id, base_color, related_color, mode in cursor.fetchall():
                grouped[base_color].append(related_color)

    logging.info(f'Load {len(grouped)} {mode.lower()} combinations from database')
    return grouped


global_monochrome = load_combinations(Mode.MONOCHROME.value)
global_complementary = load_combinations(Mode.COMPLEMENTARY.value)
global_analogous = load_combinations(Mode.ANALOGOUS.value)
