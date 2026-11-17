
async function loadSyncHistory() {
    const body = document.getElementById("sync-history-body");
    const message = document.getElementById("sync-history-message");

    if (!body || !message) {
        return;
    }

    body.replaceChildren();

    try {
        const response = await fetch("/api/sync/history?limit=10");

        if (!response.ok) {
            throw new Error("History API unavailable");
        }

        const data = await response.json();

        if (!Array.isArray(data.history)) {
            throw new Error("Invalid history response");
        }

        if (data.history.length === 0) {
            message.textContent = "No synchronization history found.";
            return;
        }

        for (const record of data.history) {
            const row = document.createElement("tr");

            const values = [
                record.finished_at ?? "--",
                record.status ?? "unknown",
                record.successful_managers ?? 0,
                record.failed_managers ?? 0,
                record.stage ?? "None",
                record.error_message || "None"
            ];

            values.forEach((value, index) => {
                const cell = document.createElement("td");
                cell.textContent = String(value);

                if (index === 1) {
                    const status = String(value).toLowerCase();

                    if (["success", "partial", "failed"].includes(status)) {
                        cell.classList.add("sync-status", `sync-status-${status}`);
                    }
                }

                row.appendChild(cell);
            });

            body.appendChild(row);
        }

        message.textContent =
            `Showing ${data.history.length} synchronization record(s).`;

    } catch (error) {
        message.textContent =
            "Synchronization history is temporarily unavailable.";
    }
}

document.addEventListener("DOMContentLoaded", loadSyncHistory);
