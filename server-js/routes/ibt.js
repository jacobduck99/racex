import path from "node:path";
import { pipeline } from "node:stream/promises";
import { createWriteStream } from "node:fs";
import fs from "node:fs/promises";
import { Telemetry } from "ibt-telemetry";
import { sendParsedIbt } from "../api/parsedTelemtryApi.js";
import { TEMP_IBT_DIR } from "../server.js";
import get_median from "../utils.js";
import buildLaps from "../dataProcessing/processTelemetry.js";

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

      const createLaps = buildLaps(telemetry);

    //const cleaned_laps = [];

    //const median = get_median(createLaps);
    //console.log("here's median", median);

    //for (let l of createLaps) {
     //   console.log("l", l);
      //  if (l <= median)
       //     cleaned_laps.push({ lapTime: l});
        //    };

    //console.log("here's cleaned_laps", cleaned_laps);

    console.log("here's the payload being sent", createLaps);

      const pyRes = await sendParsedIbt({ createLaps });
      console.log("Here's what was returned from api", pyRes);  

      return {
        ok: true,
        filename: file.filename,
        bytes: stat.size,
        lapsDetected: lapTimes.length,
        analysis: pyRes.coaching,
      };
    } finally {
      await fs.unlink(outPath).catch(() => {});
    }
  });
}
