# Meridian · identidade visual (Marco)

**Ideia:** uma linha de referência que mostra onde você está. Dois trilhos (os meridianos) e uma seta de "você está aqui" que, juntos, formam um M. Sem rosa dos ventos.

## O que tem aqui

```
guia-de-marca-meridian.pdf   guia de 8 páginas: ideia, logo, espaço e tamanhos, cores, tipografia, aplicações, o que evitar
guia-paginas/                as mesmas páginas em PNG (1280x720), para compartilhar
cores/                       paleta em PNG, TXT (HEX, RGB, CMYK aproximado) e CSS
tokens/                      tokens.css, tokens.json e tailwind.brand.js
fontes/                      Space Grotesk, Inter e JetBrains Mono (woff2/woff, só caracteres latinos) + licença OFL
redes-e-readme/              banners em SVG e PNG, versões escura e clara: imagem de prévia de link, capa do GitHub, X/Twitter, LinkedIn, cabeçalho de README e avatares
```
Os arquivos do logo estão no outro zip (`meridian-logos`).

## Cores

| Cor | HEX | Papel |
|---|---|---|
| Grafite | `#12151C` | Base: textos, trilhos do M, fundos escuros |
| Vermelhão | `#FF4500` | Destaque: a seta, item ativo, ponto de atenção |
| Papel | `#F3EFE6` | Fundo claro quente; trilhos sobre fundo escuro |
| Pedra | `#8A8578` | Apoio: texto secundário, linhas |
| Giz | `#FFFFFF` | Branco puro |

O Vermelhão é o mesmo valor do `lava` que o app já usa no `tailwind.config.js`, então a marca e a interface já combinam. As cores neutras do app (`canvas`, `card`, `raised`, `edge`, `soft`, `up`, `down`) continuam como estão.

## Tipografia

- **Space Grotesk** (500, 700): títulos, números grandes e o nome no logo.
- **Inter** (400, 500, 600): interface e texto corrido. Já é a fonte do app.
- **JetBrains Mono** (400, 500): dados, nomes de linguagem, código. Também já usada no app.

As três têm licença SIL OFL (uso comercial permitido). As fontes incluídas são o subconjunto latino; para outros alfabetos, baixe as famílias completas no Google Fonts.

## Usar no projeto

- **Tailwind:** importe `tokens/tailwind.brand.js` no `tailwind.config.js` (instruções no topo do arquivo). Adiciona `graphite`, `paper`, `stone`, `chalk` e a fonte `display`, sem mexer no que já existe.
- **CSS:** `tokens/tokens.css` traz as variáveis `--meridian-*`.
- **GitHub:** suba `redes-e-readme/github-social-1280x640-escuro.png` em Settings > Social preview e use `readme-header-1600x400-escuro.svg` (ou o claro) no topo do README.

## Observações

- O CMYK é uma conversão automática do RGB. Peça prova de cor à gráfica; Pantone não foi definido.
- Faça uma busca de anterioridade (INPI e outros países) antes de registrar a marca.
