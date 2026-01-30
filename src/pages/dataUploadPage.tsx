import { useState } from "react";

export default function DataPage() {
  const [fastLapData, setFastLapData] = useState(null);
  const [avgLapData, setAvgLapData] = useState(null);

  function handleSubmit(e) {
    e.preventDefault();

    if (!fastLapData || !avgLapData) {
      console.log("Missing file(s):", { fastLapData, avgLapData });
      return;
    }

    const fd = new FormData();
    fd.append("fastLapFile", fastLapData);
    fd.append("avgLapFile", avgLapData);

    // debug – shows what's actually being sent
    for (const [key, value] of fd.entries()) {
      console.log(key, value);
    }

    // fetch("/api/upload", { method: "POST", body: fd })
  }

  return (
    <div className="min-h-screen bg-slate-950 px-4 py-12 text-slate-100">
      <div className="mt-70 mx-auto w-full max-w-3xl">
        <div className="rounded-3xl border border-white/10 bg-white/5 p-8 shadow-2xl backdrop-blur">
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-3xl font-semibold tracking-tight">
              Upload race data
            </h1>
            <p className="mt-2 text-sm text-slate-300">
              Upload two lap exports to compare performance.
            </p>
          </div>

          <form
            onSubmit={handleSubmit}
            encType="multipart/form-data"
            className="space-y-6"
          >
            {/* Upload cards */}
            <div className="grid gap-6 sm:grid-cols-2">
              <div className="rounded-2xl border border-dashed border-white/15 bg-white/5 p-6 hover:border-white/25">
                <div className="mb-5">
                  <p className="text-base font-semibold text-slate-100">
                    Fastest lap
                  </p>
                  <p className="mt-1 text-sm text-slate-400">
                    Upload your fastest lap export (CSV / XLSX).
                  </p>
                </div>

                <input
                  type="file"
                  id="fastLapFile"
                  name="fastLapFile"
                  onChange={(e) =>
                    setFastLapData(e.target.files?.[0] ?? null)
                  }
                  className="block w-full text-sm text-slate-200
                             file:mr-4 file:rounded-xl file:border-0
                             file:bg-white/10 file:px-5 file:py-3
                             file:text-sm file:font-medium file:text-slate-100
                             hover:file:bg-white/15"
                />
              </div>

              <div className="rounded-2xl border border-dashed border-white/15 bg-white/5 p-6 hover:border-white/25">
                <div className="mb-5">
                  <p className="text-base font-semibold text-slate-100">
                    Average lap
                  </p>
                  <p className="mt-1 text-sm text-slate-400">
                    Upload your average lap export (CSV / XLSX).
                  </p>
                </div>

                <input
                  type="file"
                  id="avgLapFile"
                  name="avgLapFile"
                  onChange={(e) =>
                    setAvgLapData(e.target.files?.[0] ?? null)
                  }
                  className="block w-full text-sm text-slate-200
                             file:mr-4 file:rounded-xl file:border-0
                             file:bg-white/10 file:px-5 file:py-3
                             file:text-sm file:font-medium file:text-slate-100
                             hover:file:bg-white/15"
                />
              </div>
            </div>

            <p className="text-xs text-slate-400">
              Supported formats: CSV or XLSX. Files should come from the same
              session for best results.
            </p>

            <div className="flex items-center justify-end gap-3 pt-4">
              <button
                type="button"
                className="rounded-xl border border-white/10 bg-white/5 px-5 py-2.5 text-sm font-medium text-slate-200 hover:bg-white/10"
              >
                Cancel
              </button>

              <button
                type="submit"
                className="rounded-xl bg-indigo-500 px-5 py-2.5 text-sm font-semibold text-white
                           hover:bg-indigo-400 focus:outline-none focus:ring-2
                           focus:ring-indigo-400 focus:ring-offset-2
                           focus:ring-offset-slate-950"
              >
                Upload & Compare
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
