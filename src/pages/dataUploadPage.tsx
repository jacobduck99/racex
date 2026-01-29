import { useState, useEffect } from "react";

export default function DataPage() {
  return (
    <div className="min-h-screen bg-slate-950 px-4 py-10 text-slate-100">
      <div className="mx-auto w-full max-w-xl rounded-2xl border border-white/10 bg-white/5 p-6 shadow-lg backdrop-blur mt-80">
        <div className="mb-6">
          <h1 className="text-2xl font-semibold tracking-tight">Upload race data</h1>
          <p className="mt-1 text-sm text-slate-300">
            Choose a CSV file to import. 
          </p>
        </div>

        <form method="post" encType="multipart/form-data" className="space-y-4">
          <div className="space-y-2">
            <label htmlFor="file" className="text-sm font-medium text-slate-200">
              File
            </label>

            <div className="rounded-xl border border-dashed border-white/15 bg-white/5 p-4 hover:border-white/25">
              <input
                type="file"
                id="file"
                name="file"
                multiple
                className="block w-full text-sm text-slate-200
                           file:mr-4 file:rounded-lg file:border-0
                           file:bg-white/10 file:px-4 file:py-2
                           file:text-sm file:font-medium file:text-slate-100
                           hover:file:bg-white/15"
              />
              <p className="mt-2 text-xs text-slate-400">
                If you upload anything other than CSV it will not work.
              </p>
            </div>
          </div>

          <div className="flex items-center justify-end gap-3 pt-2">
            <button
              type="button"
              className="rounded-xl border border-white/10 bg-white/5 px-4 py-2 text-sm font-medium text-slate-200 hover:bg-white/10"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="rounded-xl bg-indigo-500 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-400 focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:ring-offset-2 focus:ring-offset-slate-950"
            >
              Upload
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}



