import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  base: './', // Relative base path ensures assets load cleanly on GitHub Pages and local servers
  server: {
    port: 3000,
    host: true
  }
});
