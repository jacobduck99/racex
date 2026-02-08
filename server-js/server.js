import Fastify from "fastify";
import cors from "@fastify/cors";
import ibtRoutes from "./routes/ibt.js";
import multipart from "@fastify/multipart";

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const fastify = Fastify({ logger: true });

await fastify.register(cors, {
  origin: "http://localhost:5173",
  methods: ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
});

fastify.register(multipart, {
  throwFileSizeLimit: true,
  limits: {
    fileSize: 200 * 1024 * 1024, // 200MB (bump as needed)
    files: 1,
    parts: 1000,
  },
});

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export const TEMP_IBT_DIR = path.join(__dirname, "tmp", "ibt");

if (!fs.existsSync(TEMP_IBT_DIR)) {
  fs.mkdirSync(TEMP_IBT_DIR, { recursive: true });
}

fastify.log.info({ TEMP_IBT_DIR }, "Temp IBT dir ready");

fastify.register(ibtRoutes, { prefix: "/api" });

const start = async () => {
  try {
    const address = await fastify.listen({ port: 3000, host: "0.0.0.0" });
    fastify.log.info(`server listening on ${address}`);
  } catch (err) {
    fastify.log.error(err);
    process.exit(1);
  }
};

start();


