import os

PASSWORD = os.getenv('PASSWORD')
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

DATABASE_PARAMS = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': PASSWORD,
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