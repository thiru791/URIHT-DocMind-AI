import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),

    {
      name: 'force-exit-after-build',
      apply: 'build',
      closeBundle() {
        setTimeout(() => process.exit(0), 0)
      },
    },
  ],
})