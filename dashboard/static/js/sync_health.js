
async function loadSyncHealth() {
    const fields = {
        status: document.getElementById("sync-status"),
        successful: document.getElementById("sync-successful"),
        failed: document.getElementById("sync-failed"),
        season: document.getElementById("sync-season"),
        finished: document.getElementById("sync-finished"),
        stage: document.getElementById("sync-stage"),
        managerIds: document.getElementById("sync-manager-ids"),
        error: document.getElementById("sync-error")
    };

    try {
        const response = await fetch("/api/sync/health");
        if (!response.ok) {
            throw new Error("Unable to load synchronization health");
        }

        const data = await response.json();

        if (data.status === "not_synchronized") {
            fields.status.textContent = "Not synchronized";
            fields.error.textContent =
                "No synchronization history found.";
            return;
        }

        fields.status.textContent = data.status || "Unknown";
        fields.successful.textContent =
            data.successful_managers ?? "--";
        fields.failed.textContent =
            data.failed_managers ?? "--";
        fields.season.textContent = data.season ?? "--";
        fields.finished.textContent = data.finished_at ?? "--";
        fields.stage.textContent = data.stage ?? "None";

        fields.managerIds.textContent =
            Array.isArray(data.failed_manager_ids) &&
            data.failed_manager_ids.length > 0
                ? data.failed_manager_ids.join(", ")
                : "None";

        fields.error.textContent = data.error_message || "";

    } catch (error) {
        fields.status.textContent = "Unavailable";
        fields.error.textContent =
            "Synchronization health is temporarily unavailable.";
    }
}

document.addEventListener("DOMContentLoaded", loadSyncHealth);
