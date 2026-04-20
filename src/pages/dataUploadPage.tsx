import { useState, useRef } from "react";
import { analyseRaceData } from "../lib/api/dataPageApi.js";
import { StepBack } from 'lucide-react';
import BuildTrackMap from "../components/trackMap.tsx";

interface CornerAnalysis {
  delta: string;
  braking: string | null;
  throttle: string | null;
  gear: string;
}

interface Coordinates {
    lon: number;
    lat: number;
}

export default function DataPage() {
    const [raceSession, setRaceSession] = useState<File | null>(null);
    const [lapsAnalysis, setLapsAnalysis] = useState<CornerAnalysis[] | null>(null);
    const [trackMap, setTrackMap] = useState<Coordinates[] | null>(null);
    const [err, setErr] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const [activeCorner, setActiveCorner] = useState(0);

    const sessionRef = useRef<HTMLInputElement>(null);

    async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
        e.preventDefault();

        if (!raceSession) {
            return;
        }
        
        setLoading(true);
        setErr(null);
        const fd = new FormData();
        fd.append("raceSession", raceSession);

        try { 
            const result = await analyseRaceData(fd);
            setLapsAnalysis(result.analysis);
            setTrackMap(result.trackMap)
        } catch (e) {
            if (e instanceof Error) {
                setErr(e.message);
            }
        } finally {
            setLoading(false);
        }
    }

    function handleCancel() {
        setRaceSession(null);
        if (sessionRef.current) sessionRef.current.value = "";
    }

if (lapsAnalysis !== null) { 
  const c = lapsAnalysis[activeCorner];
  return (
    <div className="min-h-screen min-w-full flex justify-center bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 px-2 py-10">
      <div className="">
        <div className="mb-8 mt-[1vh]">
          <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-indigo-500/20 bg-indigo-500/10 px-4 py-1.5">
            <div className="h-2 w-2 rounded-full bg-green-400 animate-pulse" />
            <span className="text-xs font-medium text-indigo-300">Analysis complete</span>
          </div>
          <h1 className="text-[2rem] font-bold tracking-tight bg-gradient-to-r from-white to-slate-300 bg-clip-text text-transparent text-center">
            Corner Analysis
          </h1>
          <p className="mt-3 text-slate-400 text-center">
            Corner-by-corner breakdown of your session.
          </p>
        </div>
        <div className="flex flex-row gap-20 mt-40 mr-20">
          <div className="flex-[5]">
            {trackMap ? <BuildTrackMap coordinates={trackMap} width={750} height={600} /> : null}
          </div>
          <div>
            <div className="rounded-2xl border border-white/10 bg-gradient-to-b from-white/10 to-white/5 p-6 backdrop-blur-xl shadow-2xl h-100 max-w-150 min-w-150">              <div className="flex items-center justify-between mb-6">
                <span className="text-sm font-medium text-indigo-300 tracking-wider uppercase">
                  Corner {activeCorner + 1}
                </span>
                <span
                  className={`text-xs font-mono font-semibold px-3 py-1 rounded-full border ${
                    parseFloat(c.delta) <= 0
                      ? "border-green-500/20 bg-green-500/10 text-green-400"
                      : "border-red-500/20 bg-red-500/10 text-red-400"
                  }`}
                >
                  {parseFloat(c.delta) <= 0 ? "" : "+"}{c.delta}s
                </span>
              </div>
              <div className="space-y-4">
                <div className="rounded-xl border border-white/10 bg-white/5 p-4">
                  <p className="text-[10px] uppercase tracking-widest text-slate-500 mb-2">Braking</p>
                  <p className="text-sm text-slate-200 leading-relaxed">{c.braking ? c.braking : "No braking in this zone"}</p>
                </div>
                <div className="rounded-xl border border-white/10 bg-white/5 p-4">
                  <p className="text-[10px] uppercase tracking-widest text-slate-500 mb-2">Throttle</p>
                  <p className="text-sm text-slate-200 leading-relaxed">{c.throttle ? c.throttle : "You were full throttle no lift detected"}</p>
                </div>
                <div className="rounded-xl border border-white/10 bg-white/5 p-4">
                  <p className="text-[10px] uppercase tracking-widest text-slate-500 mb-2">Gear</p>
                  <p className="text-sm text-slate-200 leading-relaxed">{c.gear}</p>
                </div>
              </div>
            </div>
            <div className="flex gap-2 mt-5 min-w-full w-160">
              {lapsAnalysis.map((_corner, i) => (
                <button
                  key={i}
                  onClick={() => setActiveCorner(i)}
                  className={`px-5 py-2 rounded-xl text-xs font-medium transition-all ${
                    activeCorner === i
                      ? "bg-indigo-500/20 border border-indigo-500/30 text-indigo-300"
                      : "border border-white/10 bg-white/5 text-slate-400 hover:bg-white/10 hover:text-slate-200"
                  }`}
                >
                  S{i + 1}
                </button>
              ))}
            </div>
          </div>
        </div>
        <div className="flex mt-4">
          <button
            onClick={() => setLapsAnalysis(null)}
            className="inline-flex items-center gap-2 rounded-xl border border-white/10 bg-white/5 px-5 py-2.5 text-sm font-medium text-slate-300 transition-all hover:bg-white/10 hover:text-slate-100"
          >
            <StepBack className="h-4 w-4" />
            Back
          </button>
        </div>
      </div>
    </div>
  );
}
return (
  <>
  <style>{`
    @keyframes slide {
      0% { transform: translateX(-100%); }
      100% { transform: translateX(350%); }
    }
  `}</style>
  <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 px-4 py-12">
    <div className="mx-auto w-full max-w-2xl mt-[15vh]">
      <div className="absolute inset-0 -z-10 overflow-hidden">
        <div className="absolute left-1/2 top-0 h-96 w-96 -translate-x-1/2 rounded-full bg-indigo-500/20 blur-3xl" />
      </div>

      <div className="rounded-3xl border border-white/10 bg-gradient-to-b from-white/10 to-white/5 p-8 shadow-2xl backdrop-blur-xl">
        <div className="mb-8">
          <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-indigo-500/20 bg-indigo-500/10 px-4 py-1.5">
            <div
              className={`h-2 w-2 rounded-full animate-pulse ${
                raceSession === null ? "bg-indigo-400" : "bg-green-400"
              }`}
            />
            <span className="text-xs font-medium text-indigo-300">{raceSession !== null ? "Ready to be analysed" : "Upload race file"}</span>
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
          <div className="group relative overflow-hidden rounded-2xl border border-dashed border-white/20 bg-white/5 p-8 transition-all hover:border-indigo-500/50 hover:bg-white/10">
            {loading ? (
              <div className="flex flex-col items-center justify-center py-12">
                <p className="text-sm text-indigo-300 mb-4">James is analysing your telemetry...</p>
                <div style={{ width: "100%", maxWidth: "300px", height: "4px", borderRadius: "2px", background: "#1e1e2e", overflow: "hidden" }}>
                  <div style={{
                    width: "40%",
                    height: "100%",
                    borderRadius: "2px",
                    background: "#6366f1",
                    animation: "slide 1.4s ease-in-out infinite"
                  }} />
                </div>
              </div>
            ) : (
              <>
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
                    onChange={(e) => {
                      setRaceSession(e.target.files?.[0] ?? null);
                      setErr(null);
                    }}
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
                  {err && (
                    <span className="text-sm text-red-400">{err}</span>
                  )}
                </div>
              </>
            )}
          </div>

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
              disabled={!raceSession || loading}
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
  </>
);
}
