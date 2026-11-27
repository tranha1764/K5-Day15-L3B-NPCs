import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Build ra codebase/static/ → python run.py phục vụ bản build, máy không có Node vẫn chạy được.
// npm run dev: Vite ở cổng 5173, chuyển /api sang server Python (python run.py, cổng 8000).
export default defineConfig({
  plugins: [react()],
  base: "./",
  build: {
    outDir: "../codebase/static",
    emptyOutDir: true,
  },
  server: {
    port: 5173,
    proxy: { "/api": "http://127.0.0.1:8000" },
  },
});
