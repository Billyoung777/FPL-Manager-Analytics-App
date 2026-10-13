
from database.db import get_connection


def create_tables():
    """
    Initialize the FPL Analytics database tables.
    """
    connection = get_connection()

    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS managers (
                manager_id INTEGER PRIMARY KEY,
                manager_name TEXT NOT NULL,
                team_name TEXT NOT NULL,
                last_updated TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS league_memberships (
                league_id INTEGER NOT NULL,
                manager_id INTEGER NOT NULL,
                joined_at TEXT DEFAULT CURRENT_TIMESTAMP,

                PRIMARY KEY (league_id, manager_id),

                FOREIGN KEY (league_id)
                    REFERENCES leagues(league_id),

                FOREIGN KEY (manager_id)
                    REFERENCES managers(manager_id)
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS gameweek_performances (
                manager_id INTEGER NOT NULL,
                season TEXT NOT NULL,
                gameweek INTEGER NOT NULL
                    CHECK (gameweek BETWEEN 1 AND 38),
                points INTEGER NOT NULL,
                transfer_cost INTEGER NOT NULL DEFAULT 0,
                total_points INTEGER NOT NULL,
                last_updated TEXT DEFAULT CURRENT_TIMESTAMP,

                PRIMARY KEY (manager_id, season, gameweek),

                FOREIGN KEY (manager_id)
                    REFERENCES managers(manager_id)
            )
        """)

        connection.commit()
        print("Managers table created successfully.")
        
        connection.execute("""
            CREATE TABLE IF NOT EXISTS leagues (
                league_id INTEGER PRIMARY KEY,
                league_name TEXT NOT NULL,
                last_updated TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)


    finally:
        connection.close()


if __name__ == "__main__":
    print("=" * 50)
    print("FPL DATABASE SCHEMA INITIALIZATION")
    print("=" * 50)

    create_tables()

    print("Database initialization complete.")
