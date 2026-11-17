

async function refreshSyncStatus(button) {
    if (button.disabled) {
        return;
    }

    button.disabled = true;
    button.textContent = "Refreshing...";

    const lastChecked = document.getElementById(
        "sync-last-checked"
    );

    try {
        await Promise.all([
            loadSyncHealth(),
            loadSyncHistory()
        ]);

        if (lastChecked) {
            const now = new Date();

            lastChecked.textContent =
                `Last checked: ${now.toLocaleTimeString()}`;
        }

    } catch (error) {
        if (lastChecked) {
            lastChecked.textContent =
                "Last checked: Refresh failed";
        }

    } finally {
        button.disabled = false;
        button.textContent = "Refresh Status";
    }
}


function initializeSyncRefresh() {
    const button = document.getElementById(
        "sync-refresh-button"
    );

    if (!button) {
        return;
    }

    button.addEventListener("click", () => {
        return refreshSyncStatus(button);
    });
}

document.addEventListener(
    "DOMContentLoaded",
    initializeSyncRefresh
);
