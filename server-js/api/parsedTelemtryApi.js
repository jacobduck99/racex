import dotenv from "dotenv";
dotenv.config({ path: "./server-js/.env" });

const PY_BACKEND = process.env.PY_BACKEND_URL;
console.log(process.env.PY_BACKEND_URL);

export async function sendParsedIbt(telemetry) {
    const url = `${PY_BACKEND}/api/lap-data/analyse`;
    console.log("this is url", url);

    let res;
    try {
    res = await fetch(url, {
      method: "POST",
      body: JSON.stringify(telemetry),
      headers: { "Content-Type": "application/json" },
    });
    } catch (e) {
    console.error("Network error:", e);
    throw new Error("Network error. Is Flask running on :5000?");
    }

    if (!res.ok) {
    const msg = await res.text().catch(() => "");
    throw new Error(msg || `HTTP ${res.status}`);
    }

    return await res.json();
}
