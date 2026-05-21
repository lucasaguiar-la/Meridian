/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        canvas: '#0a0a0a',
        card:   '#141414',
        raised: '#1e1e1e',
        edge:   '#2a2a2a',
        soft:   '#737373',
        lava: {
          DEFAULT: '#ff4500',
          hover:   '#ff5c1a',
          dim:     'rgba(255,69,0,0.12)',
        },
        up:   '#22c55e',
        down: '#ef4444',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'ui-monospace', 'monospace'],
      },
    },
  },
  plugins: [],
}
