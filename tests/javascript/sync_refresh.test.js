
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const scriptPath = path.resolve(
    __dirname,
    "../../dashboard/static/js/sync_refresh.js"
);

test("Refresh Status reloads health and history", async () => {
    const source = fs.readFileSync(scriptPath, "utf8");

    const calls = [];
    let clickHandler;

    const button = {
        disabled: false,
        addEventListener(event, handler) {
            if (event === "click") {
                clickHandler = handler;
            }
        }
    };

    const document = {
        getElementById(id) {
            if (id === "sync-refresh-button") {
                return button;
            }
            return null;
        },
        addEventListener(event, handler) {
            if (event === "DOMContentLoaded") {
                handler();
            }
        }
    };

    const context = {
        document,
        loadSyncHealth: async () => {
            calls.push("health");
            return true;
        },
        loadSyncHistory: async () => {
            calls.push("history");
            return true;
        }
    };

    vm.runInNewContext(source, context);

    assert.equal(typeof clickHandler, "function");

    await clickHandler();

    assert.deepEqual(calls, ["health", "history"]);
});

test("Refresh Status prevents duplicate requests", async () => {
    const source = fs.readFileSync(scriptPath, "utf8");

    let healthCalls = 0;
    let historyCalls = 0;
    let finishHealth;
    let finishHistory;

    const healthPromise = new Promise(resolve => {
        finishHealth = resolve;
    });

    const historyPromise = new Promise(resolve => {
        finishHistory = resolve;
    });

    const button = {
        disabled: false,
        textContent: "Refresh Status"
    };

    const lastChecked = {
        textContent: "Last checked: Not yet refreshed"
    };

    const document = {
        getElementById(id) {
            if (id === "sync-last-checked") {
                return lastChecked;
            }
            return null;
        },
        addEventListener() {}
    };

    const context = {
        document,
        loadSyncHealth: () => {
            healthCalls++;
            return healthPromise;
        },
        loadSyncHistory: () => {
            historyCalls++;
            return historyPromise;
        }
    };

    vm.runInNewContext(source, context);

    const firstRefresh = vm.runInNewContext(
        "refreshSyncStatus(button)",
        { ...context, button }
    );

    assert.equal(button.disabled, true);
    assert.equal(button.textContent, "Refreshing...");

    await vm.runInNewContext(
        "refreshSyncStatus(button)",
        { ...context, button }
    );

    assert.equal(healthCalls, 1);
    assert.equal(historyCalls, 1);

    finishHealth(true);
    finishHistory(true);

    await firstRefresh;

    assert.equal(button.disabled, false);
    assert.equal(button.textContent, "Refresh Status");

    assert.match(
        lastChecked.textContent,
        /^Last checked: /
    );
});

test("Refresh Status restores button after a failed request", async () => {
    const source = fs.readFileSync(scriptPath, "utf8");

    const button = {
        disabled: false,
        textContent: "Refresh Status"
    };

    const lastChecked = {
        textContent: "Last checked: Not yet refreshed"
    };

    const document = {
        getElementById(id) {
            if (id === "sync-last-checked") {
                return lastChecked;
            }
            return null;
        },
        addEventListener() {}
    };

    const context = {
        document,
        loadSyncHealth: async () => {
            throw new Error("API unavailable");
        },
        loadSyncHistory: async () => {}
    };

    vm.runInNewContext(source, context);

    await vm.runInNewContext(
        "refreshSyncStatus(button)",
        { ...context, button }
    );

    assert.equal(button.disabled, false);
    assert.equal(button.textContent, "Refresh Status");

    assert.equal(
        lastChecked.textContent,
        "Last checked: Refresh failed"
    );
});

const refreshScenarios = [
    {
        name: "Refresh Status succeeds when both loaders succeed",
        health: true,
        history: true,
        shouldSucceed: true
    },
    {
        name: "Refresh Status fails when health fails",
        health: false,
        history: true,
        shouldSucceed: false
    },
    {
        name: "Refresh Status fails when history fails",
        health: true,
        history: false,
        shouldSucceed: false
    },
    {
        name: "Refresh Status fails when both loaders fail",
        health: false,
        history: false,
        shouldSucceed: false
    }
];

for (const scenario of refreshScenarios) {
    test(scenario.name, async () => {
        const source = fs.readFileSync(scriptPath, "utf8");

        const button = {
            disabled: false,
            textContent: "Refresh Status"
        };

        const lastChecked = {
            textContent: "Last checked: Not yet refreshed"
        };

        let healthCalls = 0;
        let historyCalls = 0;

        const document = {
            getElementById(id) {
                if (id === "sync-last-checked") {
                    return lastChecked;
                }
                return null;
            },
            addEventListener() {}
        };

        const context = {
            document,
            loadSyncHealth: async () => {
                healthCalls++;
                return scenario.health;
            },
            loadSyncHistory: async () => {
                historyCalls++;
                return scenario.history;
            }
        };

        vm.runInNewContext(source, context);

        await vm.runInNewContext(
            "refreshSyncStatus(button)",
            { ...context, button }
        );

        assert.equal(healthCalls, 1);
        assert.equal(historyCalls, 1);

        assert.equal(button.disabled, false);
        assert.equal(
            button.textContent,
            "Refresh Status"
        );

        if (scenario.shouldSucceed) {
            assert.match(
                lastChecked.textContent,
                /^Last checked: (?!Refresh failed$).+/
            );
        } else {
            assert.equal(
                lastChecked.textContent,
                "Last checked: Refresh failed"
            );
        }
    });
}
