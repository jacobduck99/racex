import dotenv from "dotenv";
dotenv.config({ path: "./server-js/.env" });

const PY_BACKEND = process.env.PY_BACKEND_URL;
console.log(process.env.PY_BACKEND_URL);

export async function sendParsedIbt(telemtry) {
    const url = `${PY_BACKEND}/api/lap-data/analyse`;
    console.log("this is url", url);

    try {
    let res = await fetch(url, { method: "POST", body: telemtry,
        mode: "cors",
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
