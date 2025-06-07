import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  define: {
    global: {},
  },
  optimizeDeps: {
    include: ['buffer'],
  },
  server: {
    proxy: {
      '/xumm': {
        target: 'https://xumm.app',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/xumm/, ''),
        secure: false,
        headers: {
          'Access-Control-Allow-Origin': '*',
        },
      },
    },
  },
})


