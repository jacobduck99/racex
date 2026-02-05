const PY_BACKEND = import.meta.env.PY_BACKEND_URL;

export async function sendParsedIbt(telemtry) {
    const url = `${PY_BACKEND}/api/lap-data/analyse`;
    console.log("this is url", url);
    let res: Response;

    try {
    res = await fetch(url, { method: "POST", body: telemetry,
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
