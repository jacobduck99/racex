
export default async function ibtRoutes(fastify, opts) {
  fastify.post("/lap-data/analyse", async (request, reply) => {
    const file = await request.file();
    console.log("here's the file", file.filename, file.fieldname);
    return { filename: file.filename, fieldname: file.fieldname };
  });
}

