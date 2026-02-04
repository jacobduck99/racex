import Fastify from "fastify";
import cors from "@fastify/cors";
import ibtRoutes from "./routes/ibt.js";
import multipart from "@fastify/multipart";

const fastify = Fastify({ logger: true });

await fastify.register(cors, {
  origin: "http://localhost:5173",
  methods: ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
});

fastify.register(multipart)
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

