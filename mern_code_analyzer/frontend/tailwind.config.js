/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        display: ['Outfit', 'sans-serif'],
      },
      colors: {
        dark: {
          950: '#000000',
          900: '#111111',
          800: '#1f1f1f',
          700: '#2d2d2d',
          600: '#404040',
        },
        primary: {
          400: '#fb923c', // Orange 400
          500: '#f97316', // Orange 500
          600: '#ea580c', // Orange 600
        },
        lightPrimary: {
          500: '#171717', // Almost Black
          600: '#0a0a0a', // True Black
        }
      },
      boxShadow: {
        'glow': '0 0 40px -10px var(--tw-shadow-color)',
        'inner-light': 'inset 0 1px 0 0 rgba(255, 255, 255, 0.05)',
      },
      animation: {
        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'float': 'float 6s ease-in-out infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        }
      }
    },
  },
  plugins: [],
}
