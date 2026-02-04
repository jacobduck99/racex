
export default async function ibtRoutes(fastify, opts) {
  fastify.get("/", async () => {
    return { hello: "world" };
  });
}

