document.addEventListener("DOMContentLoaded", () => {
    const panel = document.getElementById("live-stats");

    if (!panel) return;

    const managerId = panel.dataset.managerId;
    const status = document.getElementById("live-stats-status");

    const fields = {
        overall_points: document.getElementById("overall-points"),
        overall_rank: document.getElementById("overall-rank"),
        event_points: document.getElementById("event-points"),
        current_event: document.getElementById("current-event")
    };

    const formatNumber = value =>
        value == null ? "Not available" : Number(value).toLocaleString();

    async function refreshStats() {
        try {
            const response = await fetch(
                `/api/manager/${encodeURIComponent(managerId)}/live-stats`,
                { cache: "no-store" }
            );

            if (!response.ok) {
                throw new Error("Live statistics unavailable");
            }

            const data = await response.json();

            fields.overall_points.textContent = formatNumber(data.overall_points);
            fields.overall_rank.textContent = formatNumber(data.overall_rank);
            fields.event_points.textContent = formatNumber(data.event_points);
            fields.current_event.textContent =
                data.current_event == null ? "Not available" : `GW${data.current_event}`;

            status.textContent =
                `Live data checked at ${new Date().toLocaleTimeString()}`;
        } catch (error) {
            status.textContent =
                "Unable to refresh live statistics. Retrying shortly.";
        }
    }

    refreshStats();
    setInterval(refreshStats, 60_000);
});