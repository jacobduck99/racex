import Fastify from "fastify";
import ibtRoutes from "./routes/ibt.js";
import multipart from "@fastify/multipart";

const fastify = Fastify({ logger: true });

fastify.register(ibtRoutes)
fastify.register(multipart)

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

