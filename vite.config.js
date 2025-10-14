import { defineConfig } from "vite";
import tailwindcss from "@tailwindcss/vite";
import path from "path";

export default defineConfig({
  plugins: [tailwindcss()],
  root: "./frontend",
  base: "/static/",
  build: {
    outDir: path.resolve(__dirname, "static/dist"),
    emptyOutDir: true,
    manifest: true,
    rollupOptions: {
      input: {
        main: path.resolve(__dirname, "frontend/js/main.js"),
        styles: path.resolve(__dirname, "frontend/css/main.css"),
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
      "@": path.resolve(__dirname, "frontend"),
    },
  },
});
