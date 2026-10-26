import os
from database.db import get_connection
from database.manager_analytics import calculate_manager_analytics
from database.manager_league_service import register_manager_leagues
from database.manager_repository import get_manager
from api.fpl_client import FPLClient
from database.sync_gameweeks import sync_gameweeks
from database.league_repository import get_league
from database.membership_repository import get_league_members
from database.league_member_service import synchronize_league_members
from database.gameweek_repository import get_latest_gameweek_update
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    jsonify,
)
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get(
    "FLASK_SECRET_KEY",
    "local-development-only-change-before-deployment"
)

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/enter", methods=["GET"])
def enter_manager():
    manager_id = request.args.get("id", "").strip()

    if not manager_id.isdigit() or int(manager_id) <= 0:
        return "Invalid FPL Manager ID", 400

    try:
        register_manager_leagues(int(manager_id))

    except RuntimeError:
        return "Unable to retrieve manager information from FPL", 502

    except (KeyError, TypeError, ValueError):
        return "Unexpected FPL manager information", 502

    # The manager is registered. Remember their public ID.
    session["manager_id"] = int(manager_id)

    # Synchronize available gameweek history.
    try:
        sync_gameweeks(int(manager_id), "2026/27")

    except (RuntimeError, KeyError, TypeError, ValueError) as error:
        app.logger.warning(
            "Gameweek synchronization unavailable for manager %s: %s",
            manager_id,
            error
        )

    return redirect(
        url_for("manager_dashboard", id=manager_id)
    )

    session["manager_id"] = int(manager_id)

    return redirect(
        url_for("manager_dashboard", id=manager_id)
    )


@app.route("/hub")
def manager_hub():
    manager_id = request.args.get("id", type=int)

    if manager_id is None or manager_id <= 0:
        return "Invalid FPL Manager ID", 400

    manager = get_manager(manager_id)

    if manager is None:
        return "Manager not found", 404

    try:
        leagues = FPLClient().get_manager_leagues(manager_id)
    except RuntimeError:
        return "Unable to retrieve mini-leagues from FPL", 502
    except (KeyError, TypeError, ValueError):
        return "Unexpected mini-league information", 502

    return render_template(
        "hub.html",
        manager=manager,
        leagues=leagues
    )

@app.route("/league/<int:league_id>/refresh", methods=["POST"])
def refresh_league(league_id):
    manager_id = request.form.get("manager_id", type=int)

    if manager_id is None or manager_id <= 0:
        return "Invalid FPL Manager ID", 400

    if league_id <= 0:
        return "Invalid league ID", 400

    # Confirm the selected manager belongs to this league
    # before allowing a refresh.
    members = get_league_members(league_id)

    if not any(
        member["manager_id"] == manager_id
        for member in members
    ):
        return "Manager is not a member of this league", 403

    try:
        synchronize_league_members(league_id)
    except RuntimeError:
        return "Unable to synchronize league members", 502
    except (KeyError, TypeError, ValueError):
        return "Unexpected league standings data", 502

    return redirect(
        url_for(
            "league_dashboard",
            league_id=league_id,
            manager_id=manager_id
        )
    )

@app.route("/league/<int:league_id>")
def league_dashboard(league_id):
    manager_id = request.args.get("manager_id", type=int)

    if manager_id is None or manager_id <= 0:
        return "Invalid FPL Manager ID", 400

    league = get_league(league_id)

    if league is None:
        return "League not found", 404

    members = get_league_members(league_id)

    # Only show this league in the context of a member.
    if not any(
        member["manager_id"] == manager_id
        for member in members
    ):
        return "Manager is not a member of this league", 403

    return render_template(
        "league.html",
        league=league,
        members=members,
        manager_id=manager_id
    )


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
    manager_id = request.args.get("id", type=int)

    if manager_id is None:
        manager_id = session.get("manager_id")

    if manager_id is None:
        return redirect(url_for("home"))

    if manager_id <= 0:
        return "Invalid manager ID", 400

    try:
        sync_gameweeks(manager_id, "2026/27")

    except ValueError as error:
        if get_manager(manager_id) is None:
            return "Manager not found", 404
        
        app.logger.warning(
            "Gameweek sync failed for manager %s: %s",
            manager_id,
            error
        )
    except (RuntimeError, KeyError, TypeError) as error:
        app.logger.warning(
            "Gameweek sync failed for manager %s: %s",
            manager_id,
            error
        )

    try:
        analytics = calculate_manager_analytics(
            manager_id,
            "2026/27"
        )

    except ValueError:
        manager = get_manager(manager_id)

        if manager is None:
            return "Manager not found", 404

        return render_template(
            "manager_pending.html",
            manager=manager,
            manager_id=manager_id
        )

    connection = get_connection()
    managers = connection.execute(
    """
    SELECT manager_id, manager_name, team_name
    FROM managers
    ORDER BY team_name ASC
    """
).fetchall()

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
        # Use net points for dashboard summary cards.
        # This keeps the dashboard consistent with manager analytics.
        total_points = analytics["total_net_points"]
        average_points = analytics["average_points"]
        highest_points = analytics["best_gameweek"]["points"]
        lowest_points = analytics["worst_gameweek"]["points"]
        
        gameweek_rows = connection.execute(
            """
            SELECT
                gameweek,
                points - transfer_cost AS net_points
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
            last_updated = get_latest_gameweek_update(
            manager_id,
            "2026/27"
        )



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
            cumulative_points=cumulative_points,
            managers=managers,
            selected_manager_id=manager_id,
            analytics=analytics,
            performance_trends=analytics["performance_trends"],
            last_updated=last_updated,
        )



    finally:
        connection.close()

@app.route("/profile/<int:manager_id>")
def manager_profile(manager_id):
    if manager_id <= 0:
        return "Invalid FPL Manager ID", 400

    manager = get_manager(manager_id)

    if manager is None:
        return "Manager not found", 404

    fpl_data = None

    try:
        fpl_data = FPLClient().get_manager(manager_id)
    except RuntimeError:
        app.logger.warning(
            "Live FPL data unavailable for manager %s",
            manager_id
        )

    return render_template(
        "profile.html",
        manager=manager,
        fpl_data=fpl_data
    )

@app.route("/api/manager/<int:manager_id>/live-stats")
def manager_live_stats(manager_id):
    if manager_id <= 0:
        return jsonify({"error": "Invalid FPL Manager ID"}), 400

    manager = get_manager(manager_id)

    if manager is None:
        return jsonify({"error": "Manager not found"}), 404

    try:
        fpl_data = FPLClient().get_manager(manager_id)

        return jsonify({
            "overall_points": fpl_data.get("summary_overall_points"),
            "overall_rank": fpl_data.get("summary_overall_rank"),
            "event_points": fpl_data.get("summary_event_points"),
            "current_event": fpl_data.get("current_event"),
            "updated_at": __import__("datetime").datetime.now().astimezone().isoformat()
        })

    except RuntimeError:
        app.logger.warning(
            "Live FPL stats unavailable for manager %s",
            manager_id
        )
        return jsonify({
            "error": "Live FPL statistics are temporarily unavailable"
        }), 503

if __name__ == "__main__":
    app.run(debug=True, port=5000)
