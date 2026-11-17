
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const scriptPath = path.resolve(
    __dirname,
    "../../dashboard/static/js/sync_history.js"
);

const source = fs.readFileSync(scriptPath, "utf8");

test("Synchronization History script registers a load handler", () => {
    let registeredEvent = null;
    let registeredHandler = null;

    const context = {
        document: {
            addEventListener(event, handler) {
                registeredEvent = event;
                registeredHandler = handler;
            }
        }
    };

    vm.runInNewContext(source, context);

    assert.equal(registeredEvent, "DOMContentLoaded");
    assert.equal(typeof registeredHandler, "function");
});

test("Synchronization History renders successful API records", async () => {
    const elements = {
        "sync-history-body": {
            children: [],
            replaceChildren() {
                this.children = [];
            },
            appendChild(child) {
                this.children.push(child);
            }
        },
        "sync-history-message": {
            textContent: ""
        }
    };

    const document = {
        getElementById(id) {
            return elements[id] ?? null;
        },
        createElement(tagName) {
            return {
                tagName,
                children: [],
                textContent: "",
                classList: {
                    values: [],
                    add(...classes) {
                        this.values.push(...classes);
                    }
                },
                appendChild(child) {
                    this.children.push(child);
                }
            };
        },
        addEventListener() {}
    };

    const fetch = async () => ({
        ok: true,
        json: async () => ({
            count: 1,
            history: [
                {
                    sync_id: 1,
                    season: "2026/27",
                    status: "success",
                    successful_managers: 12,
                    failed_managers: 0,
                    finished_at: "2026-10-14 14:32:57",
                    stage: null,
                    error_message: null
                }
            ]
        })
    });

    const context = { document, fetch };

    vm.runInNewContext(source, context);

    await vm.runInNewContext("loadSyncHistory()", context);

    const rows = elements["sync-history-body"].children;

    assert.equal(rows.length, 1);
    assert.equal(rows[0].tagName, "tr");
    assert.equal(rows[0].children.length, 6);

    assert.equal(
        rows[0].children[1].textContent,
        "success"
    );

    assert.equal(
        rows[0].children[2].textContent,
        "12"
    );

    assert.equal(
        rows[0].children[3].textContent,
        "0"
    );

    assert.ok(
        rows[0].children[1].classList.values.includes(
            "sync-status-success"
        )
    );

    assert.equal(
        elements["sync-history-message"].textContent,
        "Showing 1 synchronization record(s)."
    );
});

test("Synchronization History handles an empty history", async () => {
    const body = {
        children: [{ tagName: "tr" }],
        replaceChildren() {
            this.children = [];
        },
        appendChild(child) {
            this.children.push(child);
        }
    };

    const message = {
        textContent: "Loading synchronization history..."
    };

    const document = {
        getElementById(id) {
            if (id === "sync-history-body") return body;
            if (id === "sync-history-message") return message;
            return null;
        },
        addEventListener() {}
    };

    const fetch = async (url) => {
        assert.equal(url, "/api/sync/history?limit=10");

        return {
            ok: true,
            json: async () => ({
                count: 0,
                history: []
            })
        };
    };

    const context = { document, fetch };

    vm.runInNewContext(source, context);

    await vm.runInNewContext("loadSyncHistory()", context);

    assert.equal(body.children.length, 0);

    assert.equal(
        message.textContent,
        "No synchronization history found."
    );
});

test("Synchronization History handles API failures", async () => {
    const body = {
        children: [{ tagName: "tr" }],
        replaceChildren() {
            this.children = [];
        },
        appendChild(child) {
            this.children.push(child);
        }
    };

    const message = {
        textContent: "Loading synchronization history..."
    };

    const document = {
        getElementById(id) {
            if (id === "sync-history-body") return body;
            if (id === "sync-history-message") return message;
            return null;
        },
        addEventListener() {}
    };

    const fetch = async (url) => {
        assert.equal(url, "/api/sync/history?limit=10");

        return {
            ok: false,
            status: 503
        };
    };

    const context = { document, fetch };

    vm.runInNewContext(source, context);

    await vm.runInNewContext("loadSyncHistory()", context);

    assert.equal(body.children.length, 0);

    assert.equal(
        message.textContent,
        "Synchronization history is temporarily unavailable."
    );
});

test("Synchronization History safely renders error messages", async () => {
    const maliciousMessage =
        '<img src=x onerror="alert(1)">';

    const body = {
        children: [],
        replaceChildren() {
            this.children = [];
        },
        appendChild(child) {
            this.children.push(child);
        }
    };

    const message = { textContent: "" };

    const document = {
        getElementById(id) {
            if (id === "sync-history-body") return body;
            if (id === "sync-history-message") return message;
            return null;
        },

        createElement(tagName) {
            return {
                tagName,
                textContent: "",
                children: [],
                classList: {
                    add() {}
                },
                appendChild(child) {
                    this.children.push(child);
                }
            };
        },

        addEventListener() {}
    };

    const fetch = async () => ({
        ok: true,
        json: async () => ({
            count: 1,
            history: [{
                sync_id: 5,
                status: "failed",
                successful_managers: 0,
                failed_managers: 12,
                finished_at: "2026-11-17 11:30:00",
                stage: "gameweeks",
                error_message: maliciousMessage
            }]
        })
    });

    const context = { document, fetch };

    vm.runInNewContext(source, context);
    await vm.runInNewContext("loadSyncHistory()", context);

    const rows = body.children;

    assert.equal(rows.length, 1);
    assert.equal(rows[0].children.length, 6);

    const errorCell = rows[0].children[5];

    assert.equal(errorCell.textContent, maliciousMessage);
    assert.equal(errorCell.children.length, 0);

    assert.equal(
        message.textContent,
        "Showing 1 synchronization record(s)."
    );
});
