/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        saas: {
          bg: '#F8F9FC',
          'bg-dark': '#0B0F19',
          card: '#FFFFFF',
          'card-dark': '#111827',
          'card-dark-alt': '#161F30',
          border: '#E5E7EB',
          'border-dark': '#1F2937',
          'border-dark-highlight': '#334155',
          input: '#F3F4F6',
          'input-dark': '#1E293B',
          primary: '#2E31E8',
          'primary-hover': '#2326C4',
          'primary-light': '#EEF2FF',
          dark: '#0F172A',
          muted: '#64748B',
        },
      },
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
      },
      borderRadius: {
        'card': '16px',
      },
      boxShadow: {
        'card': '0 1px 3px 0 rgba(0, 0, 0, 0.05), 0 1px 2px 0 rgba(0, 0, 0, 0.03)',
        'elevated': '0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03)',
        'dark-card': '0 4px 20px -2px rgba(0, 0, 0, 0.5), 0 2px 6px -1px rgba(0, 0, 0, 0.3)',
      },
    },
  },
  plugins: [],
}
