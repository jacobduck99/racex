import path from "node:path";
import { pipeline } from "node:stream/promises";
import { createWriteStream } from "node:fs";
import fs from "node:fs/promises";
import { Telemetry } from "ibt-telemetry";
import { sendParsedIbt } from "../api/parsedTelemtryApi.js";

const TEMP_IBT_DIR = path.resolve("server-js/tmp/ibt");

export default async function ibtRoutes(fastify, opts) {
  fastify.post("/parseIbt", async (request, reply) => {
    const file = await request.file();
    const outPath = path.join(
      TEMP_IBT_DIR,
      `${Date.now()}-${Math.random().toString(16).slice(2)}.ibt`
    );

    try {
      await pipeline(file.file, createWriteStream(outPath));

      const stat = await fs.stat(outPath);
      if (stat.size < 5 * 1024 * 1024) {
        return reply.code(400).send({ error: "File too small (likely truncated)", bytes: stat.size });
      }

      const telemetry = await Telemetry.fromFile(outPath);

      const lapTimes = [];
      let prevPct = null;
      let lapStart = null;

      for (const sample of telemetry.samples()) {
        const s = sample.toJSON();
        const t = s?.SessionTime?.value;
        const pct = s?.LapDistPct?.value;

        if (typeof t !== "number" || typeof pct !== "number") continue;

        if (prevPct !== null && pct < 0.1 && prevPct > 0.9) {
          if (lapStart !== null) lapTimes.push(t - lapStart);
          lapStart = t;
        }

        prevPct = pct;
      }

      if (lapTimes.length === 0) {
        return reply.code(400).send({ error: "No laps detected" });
      }



      const pyRes = await sendParsedIbt({ lapTimes });

    console.log("sending payload keys:", Object.keys({ lapTimes }));

      return {
        ok: true,
        filename: file.filename,
        bytes: stat.size,
        lapsDetected: lapTimes.length,
        python: pyRes,
      };
    } finally {
      await fs.unlink(outPath).catch(() => {});
    }
  });
}
