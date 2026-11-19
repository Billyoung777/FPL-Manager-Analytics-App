
from database.db import get_connection


def save_manager_picks(manager_id, season, gameweek, picks):
    """
    Replace one manager's complete 15-player gameweek squad.

    All changes happen in a single transaction.
    """

    if not isinstance(manager_id, int) or manager_id <= 0:
        raise ValueError("Invalid manager ID")

    if not isinstance(gameweek, int) or not 1 <= gameweek <= 38:
        raise ValueError("Invalid gameweek")

    if not isinstance(season, str) or not season:
        raise ValueError("Invalid season")

    if not isinstance(picks, list) or len(picks) != 15:
        raise ValueError("A squad must contain exactly 15 picks")

    positions = set()
    player_ids = set()
    captain_count = 0
    vice_count = 0

    for pick in picks:
        if not isinstance(pick, dict):
            raise ValueError("Invalid pick data")

        player_id = pick.get("element")
        position = pick.get("position")
        multiplier = pick.get("multiplier")
        is_captain = pick.get("is_captain")
        is_vice = pick.get("is_vice_captain")

        if type(player_id) is not int or player_id <= 0:
            raise ValueError("Invalid player ID")

        if type(position) is not int or not 1 <= position <= 15:
            raise ValueError("Invalid squad position")

        if type(multiplier) is not int or multiplier < 0:
            raise ValueError("Invalid multiplier")

        if type(is_captain) is not bool:
            raise ValueError("Invalid captain flag")

        if type(is_vice) is not bool:
            raise ValueError("Invalid vice-captain flag")

        if is_captain and is_vice:
            raise ValueError("A player cannot hold both captain roles")

        if position in positions:
            raise ValueError("Duplicate squad position")

        if player_id in player_ids:
            raise ValueError("Duplicate player")

        positions.add(position)
        player_ids.add(player_id)
        captain_count += is_captain
        vice_count += is_vice

    if positions != set(range(1, 16)):
        raise ValueError("Squad positions must be 1 through 15")

    if captain_count != 1 or vice_count != 1:
        raise ValueError("Squad must have one captain and one vice-captain")

    connection = get_connection()

    try:
        with connection:
            connection.execute(
                """
                DELETE FROM manager_gameweek_picks
                WHERE manager_id = ?
                  AND season = ?
                  AND gameweek = ?
                """,
                (manager_id, season, gameweek)
            )

            connection.executemany(
                """
                INSERT INTO manager_gameweek_picks (
                    manager_id,
                    season,
                    gameweek,
                    player_id,
                    squad_position,
                    multiplier,
                    is_captain,
                    is_vice_captain
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        manager_id,
                        season,
                        gameweek,
                        pick["element"],
                        pick["position"],
                        pick["multiplier"],
                        int(pick["is_captain"]),
                        int(pick["is_vice_captain"])
                    )
                    for pick in picks
                ]
            )
    finally:
        connection.close()


def get_manager_picks(manager_id, season, gameweek):
    """Return saved squad picks ordered by squad position."""

    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT
                player_id,
                squad_position,
                multiplier,
                is_captain,
                is_vice_captain
            FROM manager_gameweek_picks
            WHERE manager_id = ?
              AND season = ?
              AND gameweek = ?
            ORDER BY squad_position ASC
            """,
            (manager_id, season, gameweek)
        ).fetchall()

        return [
            {
                "element": row[0],
                "position": row[1],
                "multiplier": row[2],
                "is_captain": bool(row[3]),
                "is_vice_captain": bool(row[4])
            }
            for row in rows
        ]
    finally:
        connection.close()
