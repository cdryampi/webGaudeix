import { defineConfig } from "vite";
import tailwindcss from "@tailwindcss/vite";
import path from "path";

export default defineConfig({
  plugins: [tailwindcss()],
  root: "./static/src",
  base: "/static/",
  build: {
    outDir: path.resolve(__dirname, "static/dist"),
    emptyOutDir: true,
    manifest: true,
    rollupOptions: {
      input: {
        main: path.resolve(__dirname, "static/src/js/main.js"),
      },
    },
  },
  server: {
    host: "localhost",
    port: 5173,
    strictPort: true,
    origin: "http://localhost:5173",
    cors: true,
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "static/src"),
    },
  },
});
