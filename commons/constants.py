import os

PASSWORD = os.getenv('PASSWORD')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
SUPABASE_ID = os.getenv('SUPABASE_ID')
SUPABASE_URL = f"https://{SUPABASE_ID}.supabase.co"

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_URL = 'https://generativelanguage.googleapis.com/v1beta/models'
MODEL = 'gemini-2.5-flash-lite'
# MODEL = 'gemini-2.5-flash' # 20 requests per day
HEADERS = {
    'x-goog-api-key': GEMINI_API_KEY,
    'Content-Type': 'application/json'
}

DATABASE_PARAMS = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': PASSWORD,
    'host': f"db.{SUPABASE_ID}.supabase.co",
    'port': '5432'
}

COLORS_CSV = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources', 'Colors.csv')

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
        color TEXT NOT NULL,
        tag TEXT NOT NULL
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