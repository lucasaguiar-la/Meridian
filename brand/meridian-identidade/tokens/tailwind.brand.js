// Mescle com o tailwind.config.js do frontend (mantém canvas, card, raised, edge, soft, up, down e lava como já estão).
// Uso:
//   import brand from './brand/tailwind.brand.js'
//   theme.extend.colors = { ...existentes, ...brand.colors }
//   theme.extend.fontFamily = { ...existentes, ...brand.fontFamily }
export default {
  colors: {
    graphite: '#12151C',   // Grafite
    paper: '#F3EFE6',      // Papel
    stone: '#8A8578',      // Pedra
    chalk: '#FFFFFF',      // Giz
    lava: {                // Vermelhão: igual ao `lava` que o app já usa
      DEFAULT: '#FF4500',
      hover: '#ff5c1a',
      dim: 'rgba(255,69,0,0.12)',
    },
  },
  fontFamily: {
    display: ['Space Grotesk', 'Inter', 'system-ui', 'sans-serif'],
  },
}
