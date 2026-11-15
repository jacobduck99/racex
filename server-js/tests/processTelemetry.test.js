import { test, describe } from "node:test";
import assert from "node:assert/strict";
import buildLaps, { cleanLaps } from "../dataProcessing/processTelemetry.js";

// Minimal stand-in for ibt-telemetry: samples() yields objects with getParam(name).value
const PARAM_NAMES = {
    t: "SessionTime", pct: "LapDistPct", speed: "Speed", brake: "Brake",
    throttle: "Throttle", steering: "SteeringWheelAngle", yawRate: "YawRate",
    gear: "Gear", lapDist: "LapDist", lat: "Lat", lon: "Lon",
};

function sample(t, pct, overrides = {}) {
    const values = {
        t, pct, speed: 50, brake: 0, throttle: 1, steering: 0, yawRate: 0,
        gear: 4, lapDist: pct * 4000, lat: -33.9, lon: 151.2, ...overrides,
    };
    const byParam = Object.fromEntries(
        Object.entries(PARAM_NAMES).map(([key, param]) => [param, values[key]]),
    );
    return { getParam: (name) => (name in byParam ? { value: byParam[name] } : undefined) };
}

function fakeTelemetry(samples) {
    return { samples: () => samples };
}

// One sample every `step` of lap distance from `from` to `to`, starting at time t0, 1s apart
function lapSamples(t0, from = 0.05, to = 0.95, step = 0.1) {
    const out = [];
    let t = t0;
    for (let pct = from; pct <= to + 1e-9; pct += step) out.push(sample(t++, pct));
    return out;
}

describe("buildLaps", () => {
    test("returns no laps when the start line is never crossed", () => {
        assert.deepEqual(buildLaps(fakeTelemetry(lapSamples(0))), []);
    });

    test("only counts laps that start and end on a start-line crossing", () => {
        // out-lap (partial) | full lap | full lap | in-lap (partial, never finished)
        const telemetry = fakeTelemetry([
            sample(0, 0.5), sample(1, 0.95),
            sample(2, 0.02), sample(30, 0.5), sample(60, 0.97),
            sample(62, 0.01), sample(90, 0.5), sample(121, 0.98),
            sample(123, 0.03), sample(140, 0.5),
        ]);

        const laps = buildLaps(telemetry);

        assert.equal(laps.length, 2);
        assert.deepEqual(laps.map((l) => l.lapTime), [60, 61]); // 62-2, 123-62
    });

    test("several samples just after the line count as one crossing, not many laps", () => {
        const telemetry = fakeTelemetry([
            sample(0, 0.97),
            sample(1, 0.01), sample(2, 0.04), sample(3, 0.08), // all < 0.1
            sample(30, 0.5), sample(60, 0.98),
            sample(61, 0.02), sample(62, 0.06),
        ]);

        const laps = buildLaps(telemetry);

        assert.equal(laps.length, 1);
        assert.equal(laps[0].lapTime, 60); // 61 - 1
    });

    test("skips samples with a missing or non-numeric channel", () => {
        const telemetry = fakeTelemetry([
            sample(0, 0.95),
            sample(1, 0.02),
            sample(2, 0.3),
            sample(3, 0.4, { brake: undefined }),
            sample(4, 0.5, { gear: "N" }),
            sample(5, 0.95),
            sample(6, 0.01),
        ]);

        const [lap] = buildLaps(telemetry);

        assert.ok(lap.samples.every((s) => Object.values(s).every((v) => typeof v === "number")));
        assert.ok(!lap.samples.some((s) => s.t === 3 || s.t === 4));
    });

    test("a skipped sample can't trigger a lap split", () => {
        // the only crossing sample is invalid, so no lap should be produced
        const telemetry = fakeTelemetry([
            sample(0, 0.95),
            sample(1, 0.02, { speed: null }),
            sample(2, 0.5),
        ]);
        assert.deepEqual(buildLaps(telemetry), []);
    });
});

describe("cleanLaps", () => {
    const lap = (lapTime) => ({ lapTime, samples: [] });

    test("returns [] for no laps", () => {
        assert.deepEqual(cleanLaps([]), []);
    });

    test("keeps laps within 4s of the fastest and drops the rest", () => {
        const laps = [lap(92.1), lap(90.0), lap(95.5), lap(93.9), lap(120)];
        assert.deepEqual(cleanLaps(laps).map((l) => l.lapTime), [92.1, 90.0, 93.9]);
    });

    test("a lap exactly 4s slower than the fastest is kept", () => {
        assert.equal(cleanLaps([lap(90), lap(94)]).length, 2);
    });

    test("keeps the original order", () => {
        const laps = [lap(91), lap(90), lap(92)];
        assert.deepEqual(cleanLaps(laps), laps);
    });
});
