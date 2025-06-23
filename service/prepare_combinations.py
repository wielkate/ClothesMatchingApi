import logging

import psycopg2

from commons.constants import DATABASE_PARAMS, SQL_CREATE_COMBINATIONS_TABLE, SQL_INSERT_INTO_COMBINATIONS_TABLE
from service import global_colors
from models.Mode import Mode

logger = logging.getLogger(__name__)


def save_to_database(data: list):
    with psycopg2.connect(**DATABASE_PARAMS) as connection:
        with connection.cursor() as cursor:
            cursor.execute(SQL_CREATE_COMBINATIONS_TABLE)
            cursor.executemany(SQL_INSERT_INTO_COMBINATIONS_TABLE, data)
        connection.commit()
        logger.info(f"Saved {len(data)} combinations to database")


def are_monochromatic(hsv1, hsv2, hue_threshold=10, saturation_threshold=20):
    h1, s1, v1 = hsv1
    h2, s2, v2 = hsv2

    # Check if hue difference is small (same color family)
    hue_match = abs(h1 - h2) <= hue_threshold or abs(h1 - h2) >= (360 - hue_threshold)

    # Check if saturation difference is reasonable
    saturation_match = abs(s1 - s2) <= saturation_threshold

    return hue_match and saturation_match


def monochrome_for(for_color):
    return [[for_color.name, color.name, Mode.MONOCHROME.value] for color in global_colors if
            are_monochromatic(color.hsv, for_color.hsv)]


def are_analogous(hsv1, hsv2, hue_min_threshold=10, hue_max_threshold=40, saturation_threshold=20,
                  value_threshold=20):
    h1, s1, v1 = hsv1
    h2, s2, v2 = hsv2

    # Calculate hue difference with wrap-around
    hue_diff = abs(h1 - h2)
    hue_diff = 360 - hue_diff if hue_diff > 180 else hue_diff

    # Check thresholds
    hue_match = hue_min_threshold <= hue_diff <= hue_max_threshold
    saturation_match = abs(s1 - s2) <= saturation_threshold
    value_match = abs(v1 - v2) <= value_threshold

    return hue_match and saturation_match and value_match


def analogous_for(for_color):
    return [[for_color.name, color.name, Mode.ANALOGOUS.value] for color in global_colors if
            are_analogous(color.hsv, for_color.hsv)]


def are_complementary(hsv1, hsv2, hue_threshold=20, saturation_threshold=20, value_threshold=20):
    h1, s1, v1 = hsv1
    h2, s2, v2 = hsv2

    # Calculate hue difference with wrap-around
    hue_diff = abs(h1 - h2)
    hue_diff = 360 - hue_diff if hue_diff > 180 else hue_diff

    # Check thresholds
    hue_match = abs(hue_diff - 180) <= hue_threshold
    saturation_match = abs(s1 - s2) <= saturation_threshold
    value_match = abs(v1 - v2) <= value_threshold

    return hue_match and saturation_match and value_match


def complementary_for(for_color):
    return [[for_color.name, color.name, Mode.COMPLEMENTARY.value] for color in global_colors if
            are_complementary(color.hsv, for_color.hsv)]


def prepare_combinations():
    color_modes = (monochrome_for, complementary_for, analogous_for)
    data = [
        row
        for mode in color_modes
        for color in global_colors
        for row in mode(color)
    ]
    save_to_database(data)
