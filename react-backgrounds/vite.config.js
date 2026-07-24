import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  define: {
    'process.env.NODE_ENV': JSON.stringify('production')
  },
  build: {
    lib: {
      entry: path.resolve(__dirname, 'src/main.jsx'),
      name: 'ReactBackgrounds',
      fileName: (format) => `react-backgrounds.${format}.js`,
      formats: ['umd']
    },
    outDir: path.resolve(__dirname, '../static/js'),
    emptyOutDir: false,
    rollupOptions: {
      // Inline all dependencies so it is self-contained and loads easily in standard Django templates.
    }
  }
});
