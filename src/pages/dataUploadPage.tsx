import { useState, useRef } from "react";
import { analyseRaceData } from "../lib/api/dataPageApi.js";

export default function DataPage() {
    const [raceSession, setRaceSession] = useState(null);

    const sessionRef = useRef(null);

    async function handleSubmit(e) {
        e.preventDefault();

    if (!raceSession) {
      console.log("Missing file:", { raceSession });
      return;
    }

    const fd = new FormData();
    fd.append("raceSession", raceSession );

    for (const [key, value] of fd.entries()) {
      console.log(key, value);
    }

    try { 
        const result = await analyseRaceData(fd);
        
        } catch (e) {
            console.log("error", e.message);
        }
  }

    function handleCancel() {
        setRaceSession(null);

        if (sessionRef.current) sessionRef.current.value = "";
    }

return (
  <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 px-4 py-12">
    <div className="mx-auto w-full max-w-2xl mt-50">
      {/* Decorative glow effect */}
      <div className="absolute inset-0 -z-10 overflow-hidden">
        <div className="absolute left-1/2 top-0 h-96 w-96 -translate-x-1/2 rounded-full bg-indigo-500/20 blur-3xl" />
      </div>

      <div className="rounded-3xl border border-white/10 bg-gradient-to-b from-white/10 to-white/5 p-8 shadow-2xl backdrop-blur-xl">
        {/* Header */}
        <div className="mb-8">
          <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-indigo-500/20 bg-indigo-500/10 px-4 py-1.5">
            <div className="h-2 w-2 rounded-full bg-indigo-400 animate-pulse" />
            <span className="text-xs font-medium text-indigo-300">Telemetry Analysis</span>
          </div>
          <h1 className="text-4xl font-bold tracking-tight bg-gradient-to-r from-white to-slate-300 bg-clip-text text-transparent">
            Upload Race Data
          </h1>
          <p className="mt-3 text-slate-400">
            Upload your session to compare performance and analyze telemetry.
          </p>
        </div>

        <form
          onSubmit={handleSubmit}
          encType="multipart/form-data"
          className="space-y-6"
        >
          {/* Upload card */}
          <div className="group relative overflow-hidden rounded-2xl border border-dashed border-white/20 bg-white/5 p-8 transition-all hover:border-indigo-500/50 hover:bg-white/10">
            {/* Hover gradient effect */}
            <div className="absolute inset-0 bg-gradient-to-r from-indigo-500/0 via-indigo-500/5 to-indigo-500/0 opacity-0 transition-opacity group-hover:opacity-100" />
            
            <div className="relative">
              <div className="mb-6 flex items-center gap-4">
                <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-indigo-500 to-indigo-600 shadow-lg shadow-indigo-500/25">
                  <svg className="h-7 w-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                  </svg>
                </div>
                <div>
                  <p className="text-lg font-semibold text-slate-100">
                    Racing Session
                  </p>
                  <p className="mt-1 text-sm text-slate-400">
                    Upload telemetry export (.ibt file)
                  </p>
                </div>
              </div>

              <input
                ref={sessionRef}
                type="file"
                id="raceSession"
                name="raceSessionFile"
                onChange={(e) =>
                  setRaceSession(e.target.files?.[0] ?? null)
                }
                className="block w-full cursor-pointer text-sm text-slate-200
                           file:mr-4 file:cursor-pointer file:rounded-xl file:border-0
                           file:bg-gradient-to-r file:from-indigo-500 file:to-indigo-600 file:px-6 file:py-3
                           file:text-sm file:font-semibold file:text-white file:shadow-lg
                           file:shadow-indigo-500/25 file:transition-all
                           hover:file:from-indigo-400 hover:file:to-indigo-500 hover:file:shadow-xl
                           hover:file:shadow-indigo-500/30"
              />
              
              {raceSession && (
                <div className="mt-4 flex items-center gap-2 rounded-lg bg-indigo-500/10 border border-indigo-500/20 px-4 py-2.5">
                  <svg className="h-5 w-5 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span className="text-sm font-medium text-indigo-300">{raceSession.name}</span>
                </div>
              )}
            </div>
          </div>

          {/* Info banner */}
          <div className="flex gap-3 rounded-xl border border-blue-500/20 bg-blue-500/5 p-4">
            <svg className="h-5 w-5 flex-shrink-0 text-blue-400 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p className="text-sm text-slate-300">
              <span className="font-medium text-slate-200">Supported format:</span> iRacing .ibt files found at 
              <code className="mx-1 rounded bg-white/10 px-1.5 py-0.5 text-xs font-mono text-slate-200">
                documents/iracing/telemetry
              </code>
            </p>
          </div>

          {/* Action buttons */}
          <div className="flex items-center justify-end gap-3 pt-4">
            <button 
              onClick={handleCancel}
              type="button"
              className="rounded-xl border border-white/10 bg-white/5 px-6 py-2.5 text-sm font-medium text-slate-200 transition-all hover:bg-white/10 hover:border-white/20"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={!raceSession}
              className="rounded-xl bg-gradient-to-r from-indigo-500 to-indigo-600 px-6 py-2.5 text-sm font-semibold text-white
                         shadow-lg shadow-indigo-500/25 transition-all
                         hover:from-indigo-400 hover:to-indigo-500 hover:shadow-xl hover:shadow-indigo-500/30
                         focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:ring-offset-2
                         focus:ring-offset-slate-950 disabled:opacity-50 disabled:cursor-not-allowed
                         disabled:hover:from-indigo-500 disabled:hover:to-indigo-600"
            >
              Upload
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
);
}
