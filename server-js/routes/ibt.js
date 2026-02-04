
export default async function ibtRoutes(fastify, opts) {
  fastify.post("/lap-data/analyse", async (request, reply) => {
    const file = await request.file();
    return { filename: file.filename, fieldname: file.fieldname };
  });
}

