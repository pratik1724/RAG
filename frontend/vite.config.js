import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,          // matches the dev output you shared
    strictPort: true,    // fail if 3000 is taken (helps avoid confusion)
  }
})
