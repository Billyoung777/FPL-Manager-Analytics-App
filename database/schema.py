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
            CREATE TABLE IF NOT EXISTS leagues (
                league_id INTEGER PRIMARY KEY,
                league_name TEXT NOT NULL,
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

        connection.execute("""
            CREATE TABLE IF NOT EXISTS sync_history (
                sync_id INTEGER PRIMARY KEY AUTOINCREMENT,
                season TEXT NOT NULL,
                status TEXT NOT NULL,
                successful_managers INTEGER DEFAULT 0,
                failed_managers INTEGER DEFAULT 0,
                started_at TEXT NOT NULL,
                finished_at TEXT NOT NULL
            )
        """)

        # Store historical FPL squad selections.
        connection.execute("""
            CREATE TABLE IF NOT EXISTS manager_gameweek_picks (
                manager_id INTEGER NOT NULL,
                season TEXT NOT NULL,
                gameweek INTEGER NOT NULL
                    CHECK (gameweek BETWEEN 1 AND 38),
                player_id INTEGER NOT NULL,
                squad_position INTEGER NOT NULL
                    CHECK (squad_position BETWEEN 1 AND 15),
                multiplier INTEGER NOT NULL DEFAULT 1
                    CHECK (multiplier >= 0),
                is_captain INTEGER NOT NULL DEFAULT 0
                    CHECK (is_captain IN (0, 1)),
                is_vice_captain INTEGER NOT NULL DEFAULT 0
                    CHECK (is_vice_captain IN (0, 1)),
                last_updated TEXT DEFAULT CURRENT_TIMESTAMP,

                PRIMARY KEY (
                    manager_id,
                    season,
                    gameweek,
                    squad_position
                ),

                UNIQUE (
                    manager_id,
                    season,
                    gameweek,
                    player_id
                ),

                FOREIGN KEY (manager_id)
                    REFERENCES managers(manager_id)
            )
        """)

        # Track synchronization and finalization of historical squads.
        connection.execute("""
            CREATE TABLE IF NOT EXISTS manager_squad_sync_status (
                manager_id INTEGER NOT NULL,
                season TEXT NOT NULL,
                gameweek INTEGER NOT NULL
                    CHECK (gameweek BETWEEN 1 AND 38),
                is_final INTEGER NOT NULL DEFAULT 0
                    CHECK (is_final IN (0, 1)),
                last_synced_at TEXT NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,

                PRIMARY KEY (
                    manager_id,
                    season,
                    gameweek
                ),

                FOREIGN KEY (manager_id)
                    REFERENCES managers(manager_id)
            )
        """)

        # Upgrade existing sync_history tables without deleting records.
        existing_columns = {
            row[1]
            for row in connection.execute(
                "PRAGMA table_info(sync_history)"
            ).fetchall()
        }

        new_columns = {
            "stage": "TEXT",
            "error_message": "TEXT",
            "failed_manager_ids": "TEXT"
        }

        for column_name, column_type in new_columns.items():
            if column_name not in existing_columns:
                connection.execute(
                    f"ALTER TABLE sync_history "
                    f"ADD COLUMN {column_name} {column_type}"
                )

        connection.commit()

        print("All database tables initialized successfully.")

    finally:
        connection.close()


if __name__ == "__main__":
    print("=" * 50)
    print("FPL DATABASE SCHEMA INITIALIZATION")
    print("=" * 50)

    create_tables()

    print("Database initialization complete.")
