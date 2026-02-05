import path from "node:path";
import { pipeline } from "node:stream/promises";
import { createWriteStream } from "node:fs";
import fs from "node:fs/promises";
import { Telemetry } from "ibt-telemetry";
import { sendParsedIbt } from "../api/parsedTelemtryApi.js";

const TEMP_IBT_DIR = path.resolve("server-js/tmp/ibt");

export default async function ibtRoutes(fastify, opts) {
  fastify.post("/parseIbt", async (request, reply) => {
    const file = await request.file(); // multipart file object

    const id = `${Date.now()}-${Math.random().toString(16).slice(2)}`;
    const outPath = path.join(TEMP_IBT_DIR, `${id}.ibt`);

    fastify.log.info({ outPath, original: file.filename }, "Saving upload to temp");

    try {
        await pipeline(file.file, createWriteStream(outPath));

        fastify.log.info({ outPath }, "Upload saved, ready to parse");
      
        const telemetry = await Telemetry.fromFile(outPath);

        const telemetryValues = []; 
        for (const sample of telemetry.samples()) {
          const time = sample.getParam("SessionTime")?.value;
          const lap = sample.getParam("Lap")?.value;
          const dist = sample.getParam("LapDistPct")?.value;
          const speed = sample.getParam("Speed")?.value;
          const brake = sample.getParam("Brake")?.value;
          const throttle = sample.getParam("Throttle")?.value;

          if (time !== undefined && lap !== undefined && dist !== undefined) {
            telemetryValues.push({
              t: time,
              lap,
              dist,
              speed,
              brake,
              throttle,
            });
          }
        }

        await sendParsedIbt(telemetryValues);

      return { savedTo: outPath, filename: file.filename, fieldname: file.fieldname };
    } finally {

      await fs.unlink(outPath).catch(() => {});
    }
  });
}

