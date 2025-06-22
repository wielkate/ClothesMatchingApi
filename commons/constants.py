import os

DATABASE_PARAMS = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': os.getenv('PASSWORD'),
    'host': 'db.fvhfcvqhlrfhwxgqkhan.supabase.co',
    'port': '5432'
}

COLORS_CSV = 'resources/Colors.csv'

SQL_CREATE_COLORS_TABLE = """
    CREATE TABLE IF NOT EXISTS colors (
        color TEXT PRIMARY KEY,
        r INTEGER NOT NULL,
        g INTEGER NOT NULL,
        b INTEGER NOT NULL
    )
"""
SQL_CREATE_COMBINATIONS_TABLE = """
    CREATE TABLE IF NOT EXISTS combinations (
        id SERIAL PRIMARY KEY,
        color TEXT NOT NULL,
        related_color TEXT NOT NULL,
        mode TEXT CHECK (mode IN ('Monochrome', 'Analogous', 'Complementary'))
    )
"""
SQL_CREATE_CLOTHES_TABLE = """
    CREATE TABLE IF NOT EXISTS clothes (
        filename TEXT PRIMARY KEY,
        color TEXT NOT NULL
    )
"""

SQL_INSERT_INTO_COLORS_TABLE = """
    INSERT INTO colors (color, r, g, b)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (color) DO NOTHING
"""
SQL_INSERT_INTO_COMBINATIONS_TABLE = """
    INSERT INTO combinations (color, related_color, mode)
    VALUES (%s, %s, %s)
"""
SQL_INSERT_INTO_CLOTHES_TABLE = """
    INSERT INTO clothes (filename, color)
    VALUES (%s, %s)
    ON CONFLICT (filename) DO UPDATE SET color = EXCLUDED.color
"""

SQL_GET_ALL_COLORS = "SELECT * FROM colors"
SQL_GET_COMBINATIONS_BY_MODE = """
    SELECT * FROM combinations
    WHERE mode = %s
"""
SQL_GET_ALL_CLOTHES_ITEMS = "SELECT * FROM clothes"

SQL_UPDATE_CLOTHES_TABLE = """
    UPDATE clothes
    SET color = %s
    WHERE filename = %s
"""

SQL_DELETE_FROM_CLOTHES_TABLE = """
    DELETE FROM clothes
    WHERE filename = %s
"""
