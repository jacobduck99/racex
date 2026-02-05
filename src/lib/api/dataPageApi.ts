const API_BASE = import.meta.env.VITE_API_URL;

export async function analyseRaceData(session: FormData) {
    const url = `${API_BASE}/api/parseIbt`;
    console.log("this is url", url);
    let res: Response;

    try {
    res = await fetch(url, { method: "POST", body: session,
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
