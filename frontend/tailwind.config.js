/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        // Identidade "Marco" (brand/meridian-identidade)
        graphite: '#12151C', // Grafite
        paper:    '#F3EFE6', // Papel
        stone:    '#8A8578', // Pedra
        chalk:    '#FFFFFF', // Giz

        // Superfícies do app (escuro). canvas/soft vêm do guia;
        // card/raised/edge são tons derivados do Grafite.
        canvas: '#12151C',
        card:   '#191D26',
        raised: '#222732',
        edge:   '#2E3440',
        soft:   '#8A8578',
        lava: {
          DEFAULT: '#FF4500', // Vermelhão
          hover:   '#ff5c1a',
          dim:     'rgba(255,69,0,0.12)',
        },
        up:   '#22c55e',
        down: '#ef4444',
      },
      fontFamily: {
        display: ['Space Grotesk', 'Inter', 'system-ui', 'sans-serif'],
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'ui-monospace', 'monospace'],
      },
    },
  },
  plugins: [],
}
