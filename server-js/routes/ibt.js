import { Telemetry } from "ibt-telemetry";
import { sendParsedIbt } from "../api/parsedTelemtryApi.js";
import { TEMP_IBT_DIR } from "../server.js";
import buildLaps, { cleanLaps } from "../dataProcessing/processTelemetry.js";
import saveUpload from "../uploads/saveUpload.js";
import fs from "node:fs/promises";

const MAX_IBT_BYTES = 200 * 1024 * 1024;
const MIN_IBT_BYTES = 100 * 1024;

export default async function ibtRoutes(fastify, opts) {
  fastify.post(
    "/parseIbt",
    { bodyLimit: MAX_IBT_BYTES },
    async (request, reply) => {
      const file = await request.file();
      const { path, bytes } = await saveUpload(file, {
        tempDir: TEMP_IBT_DIR,
        extension: ".ibt",
        min_bytes: MIN_IBT_BYTES,
      });

      try {
        const telemetry = await Telemetry.fromFile(path);
        const laps = buildLaps(telemetry);
        const cleaned = cleanLaps(laps);

        request.log.debug({ lapCount: cleaned.length }, "parsed ibt");

        const pyres = await sendParsedIbt(cleaned);

        return {
          ok: true,
          filename: file.filename,
          bytes: bytes,
          lapsDetected: cleaned.length,
          analysis: pyres.coaching,
          trackMap: pyres.track_map,
        };
      } catch (err) {
        request.log.error({ err }, "ibt parse failed");
        return reply.code(500).send({ ok: false, error: "parse_failed" });
      } finally {
        await fs.unlink(path).catch(() => {});
      }
    }
  );
};
