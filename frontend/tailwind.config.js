/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        surface: {
          DEFAULT: '#131313',
          dim: '#131313',
          bright: '#393939',
          lowest: '#0E0E0E',
          low: '#1C1B1B',
          container: '#201F1F',
          high: '#2A2A2A',
          highest: '#353534',
        },
        primary: {
          DEFAULT: '#EFFFE3',
          container: '#39FF14',
          fixed: '#79FF5B',
          'fixed-dim': '#2AE500',
        },
        secondary: {
          DEFAULT: '#B0C6FF',
          container: '#568DFF',
        },
        tertiary: {
          DEFAULT: '#FFF9F7',
          container: '#FFD4CB',
        },
        error: {
          DEFAULT: '#FFB4AB',
          container: '#93000A',
        },
        macro: {
          protein: '#39FF14',
          carbs: '#568DFF',
          fats: '#FFB4A4',
        },
      },
      fontFamily: {
        sans: ['Plus Jakarta Sans', 'system-ui', 'sans-serif'],
      },
      spacing: {
        '18': '4.5rem',
        '22': '5.5rem',
      },
      borderRadius: {
        'xl': '12px',
        '2xl': '16px',
        '3xl': '24px',
      },
      boxShadow: {
        'neon': '0 0 20px rgba(57, 255, 20, 0.15), 0 0 40px rgba(57, 255, 20, 0.05)',
        'glow': '0 0 40px rgba(239, 255, 227, 0.04)',
        'card': '0 4px 20px rgba(0, 0, 0, 0.3)',
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'float': 'float 3s ease-in-out infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-5px)' },
        },
      },
    },
  },
  plugins: [],
}