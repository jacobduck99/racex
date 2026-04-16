import path from "node:path";
import { createWriteStream } from "node:fs";
import fs from "node:fs/promises";
import { pipeline } from "node:stream/promises";

export default async function saveUpload(file, { tempDir, extension, minBytes = 0 }) {
    const outPath = path.join(
        tempDir,
        `${Date.now()}-${Math.random().toString(16).slice(2)}${extension}`
    );
    await pipeline(file.file, createWriteStream(outPath));
    const stat = await fs.stat(outPath);
    if (stat.size < minBytes) {
        await fs.unlink(outPath).catch(() => {});
        throw new Error(`File too small (${stat.size} bytes, minimum ${minBytes})`);
    }
    return { path: outPath, bytes: stat.size };
}
