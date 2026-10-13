
import sqlite3
from pathlib import Path


# Get the root directory of our FPL project
BASE_DIR = Path(__file__).resolve().parent.parent

# Store the database inside the database folder
DATABASE_PATH = BASE_DIR / "database" / "fpl_analytics.db"


def get_connection():
    """
    Create and return a connection to the SQLite database.
    """
    connection = sqlite3.connect(DATABASE_PATH)

    # Enable foreign key constraints
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


if __name__ == "__main__":
    print("=" * 50)
    print("FPL DATABASE CONNECTION TEST")
    print("=" * 50)

    connection = get_connection()

    print("Database connection: SUCCESS")
    print(f"Database location: {DATABASE_PATH}")

    connection.close()

    print("Database connection closed successfully.")
