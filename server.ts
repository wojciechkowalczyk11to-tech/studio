import express from "express";
import { createServer as createViteServer } from "vite";
import archiver from "archiver";
import path from "path";
import fs from "fs";

async function startServer() {
  const app = express();
  const PORT = 3000;

  // API route to download the modified repository
  app.get("/api/download", (req, res) => {
    const repoPath = path.resolve(process.cwd(), "repo_content");
    
    if (!fs.existsSync(repoPath)) {
      return res.status(404).send("Repository not found");
    }

    res.attachment("NOC-fixed.zip");
    const archive = archiver("zip", {
      zlib: { level: 9 }
    });

    archive.on("error", (err) => {
      res.status(500).send({ error: err.message });
    });

    archive.pipe(res);
    archive.directory(repoPath, false);
    archive.finalize();
  });

  // Vite middleware for development
  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    app.use(express.static("dist"));
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`Server running on http://localhost:${PORT}`);
  });
}

startServer();
