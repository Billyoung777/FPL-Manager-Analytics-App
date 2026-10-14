from flask import Flask, render_template
from database.db import get_connection

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <h1>NoDNA Just DiskiAura</h1>
    <h2>FPL Manager Analytics Dashboard</h2>
    <p>Welcome to our Fantasy Premier League Analytics System!</p>
    <p>Milestone 6: Dashboard Development</p>
    """


@app.route("/database-test")
def database_test():
    connection = get_connection()

    try:
        cursor = connection.execute(
            "SELECT COUNT(*) FROM managers"
        )
        manager_count = cursor.fetchone()[0]

        return (
            "<h1>Database Connection Successful!</h1>"
            f"<p>Total Managers: {manager_count}</p>"
        )

    finally:
        connection.close()


@app.route("/manager")
def manager_dashboard():
    manager_id = 1053858

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT
                m.manager_name,
                m.team_name,
                COUNT(g.gameweek) AS gameweeks,
                COALESCE(SUM(g.points), 0) AS total_points
            FROM managers AS m
            LEFT JOIN gameweek_performances AS g
                ON m.manager_id = g.manager_id
                AND g.season = ?
            WHERE m.manager_id = ?
            GROUP BY m.manager_id, m.manager_name, m.team_name
            """,
            ("2026/27", manager_id)
        )

        result = cursor.fetchone()

        if result is None:
            return "Manager not found", 404

        manager_name, team_name, gameweeks, total_points = result
        
        performance = connection.execute(
            """
            SELECT
                ROUND(AVG(points), 2) AS average_points,
                MAX(points) AS highest_points,
                MIN(points) AS lowest_points
            FROM gameweek_performances
            WHERE manager_id = ?
              AND season = ?
            """,
            (manager_id, "2026/27")
        ).fetchone()

        average_points, highest_points, lowest_points = performance
        
        gameweek_rows = connection.execute(
            """
            SELECT gameweek, points
            FROM gameweek_performances
            WHERE manager_id = ?
              AND season = ?
            ORDER BY gameweek ASC
            """,
            (manager_id, "2026/27")
        ).fetchall()

        gameweek_labels = [
            f"GW{row[0]}" for row in gameweek_rows
        ]

        gameweek_points = [
            row[1] for row in gameweek_rows
        ]
        
        cumulative_points = []
        running_total = 0

        for points in gameweek_points:
            running_total += points
            cumulative_points.append(running_total)



        return render_template(
            "manager.html",
            manager_name=manager_name,
            team_name=team_name,
            gameweeks=gameweeks,
            total_points=total_points,
            average_points=average_points,
            highest_points=highest_points,
            lowest_points=lowest_points,
            gameweek_labels=gameweek_labels,
            gameweek_points=gameweek_points,
            cumulative_points=cumulative_points
        )



    finally:
        connection.close()


if __name__ == "__main__":
    app.run(debug=True, port=5000)
