import { defineConfig } from 'vite';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

// Serve the Python composer's actual output, including all native multipage routes.
// Production stays a static site; Vite is the development and browser-QA surface.
export default defineConfig({
  root: 'dist',
  cacheDir: fileURLToPath(new URL('./node_modules/.vite', import.meta.url)),
  publicDir: false,
  appType: 'mpa',
  plugins: [{name:'viewport-review',configureServer(server){
    server.middlewares.use('/__review', (_request,response) => {
      response.setHeader('Content-Type','text/html; charset=utf-8');
      response.end(readFileSync(new URL('./tests/viewport-review.html',import.meta.url),'utf8'));
    });
  }}],
  server: {
    host: '0.0.0.0',
    allowedHosts: ['terminal.local'],
    fs: { strict: true },
  },
});
