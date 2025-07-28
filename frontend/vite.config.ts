import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    port: 5173,
    proxy: {
      "/api": {
        target: "http://localhost:8000/api",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
      "/dev": {
        target: "http://localhost:8000/dev",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/dev/, ""),
      },
      "/ws": {
        target: "ws://localhost:8000/ws",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/ws/, ""),
        ws: true,
      },
    },
  },
});
