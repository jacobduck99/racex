import path from "node:path";
import { pipeline } from "node:stream/promises";
import { createWriteStream } from "node:fs";
import fs from "node:fs/promises";

const TEMP_IBT_DIR = path.resolve("server-js/tmp/ibt");

export default async function ibtRoutes(fastify, opts) {
  fastify.post("/lap-data/analyse", async (request, reply) => {
    const file = await request.file(); // multipart file object

    const id = `${Date.now()}-${Math.random().toString(16).slice(2)}`;
    const outPath = path.join(TEMP_IBT_DIR, `${id}.ibt`);

    fastify.log.info({ outPath, original: file.filename }, "Saving upload to temp");

    try {
      await pipeline(file.file, createWriteStream(outPath));

      fastify.log.info({ outPath }, "Upload saved, ready to parse");


      return { savedTo: outPath, filename: file.filename, fieldname: file.fieldname };
    } finally {

      await fs.unlink(outPath).catch(() => {});
    }
  });
}

