/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#0a0a0f',
        surface: '#111827',
        border: '#1f2937',
      },
    },
  },
  plugins: [],
}

// Extended with landing page utilities
